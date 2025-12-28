from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from .models import Event, Enrollment
from .serializers import EventSerializer, EventListSerializer, EnrollmentSerializer
from accounts.permissions import IsVerified, IsSeeker, IsFacilitator, IsEventOwner


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for Event CRUD operations."""
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, IsVerified]

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        return EventSerializer

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsVerified(), IsFacilitator()]
        return super().get_permissions()

    def get_queryset(self):
        """Filter queryset based on user role and search params."""
        queryset = super().get_queryset()

        # If facilitator, show only their events
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'Facilitator':
            if self.action == 'list':
                queryset = queryset.filter(created_by=self.request.user)

        # If seeker, apply search filters
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'Seeker':
            location = self.request.query_params.get('location')
            language = self.request.query_params.get('language')
            starts_after = self.request.query_params.get('starts_after')
            starts_before = self.request.query_params.get('starts_before')
            q = self.request.query_params.get('q')  # Search in title/description

            if location:
                queryset = queryset.filter(location__icontains=location)
            if language:
                queryset = queryset.filter(language__icontains=language)
            if starts_after:
                try:
                    starts_after_dt = timezone.datetime.fromisoformat(starts_after.replace('Z', '+00:00'))
                    queryset = queryset.filter(starts_at__gte=starts_after_dt)
                except ValueError:
                    pass
            if starts_before:
                try:
                    starts_before_dt = timezone.datetime.fromisoformat(starts_before.replace('Z', '+00:00'))
                    queryset = queryset.filter(starts_at__lte=starts_before_dt)
                except ValueError:
                    pass
            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q) | Q(description__icontains=q)
                )

            # Order by upcoming first
            queryset = queryset.order_by('starts_at')

        return queryset

    def perform_create(self, serializer):
        """Set created_by to current user."""
        serializer.save(created_by=self.request.user)

    def get_object(self):
        """Override to check ownership for update/delete."""
        obj = super().get_object()
        if self.action in ['update', 'partial_update', 'destroy']:
            if obj.created_by != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You can only modify events you created.")
        return obj

    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get enrollments for a specific event (Facilitator only)."""
        event = self.get_object()
        if event.created_by != request.user:
            return Response(
                {'detail': 'You can only view enrollments for your own events.', 'code': 'permission_denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        enrollments = event.enrollments.filter(status='enrolled')
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment operations (Seeker only)."""
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsSeeker]

    def get_queryset(self):
        """Return enrollments for the current seeker."""
        return Enrollment.objects.filter(seeker=self.request.user)

    def get_serializer_context(self):
        """Add context to serializer."""
        context = super().get_serializer_context()
        if 'event_id' in self.kwargs:
            try:
                context['event'] = Event.objects.get(pk=self.kwargs['event_id'])
            except Event.DoesNotExist:
                pass
        return context

    @action(detail=False, methods=['get'])
    def past(self, request):
        """List past enrollments (events already ended)."""
        now = timezone.now()
        enrollments = self.get_queryset().filter(
            event__ends_at__lt=now,
            status='enrolled'
        )
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """List upcoming enrollments."""
        now = timezone.now()
        enrollments = self.get_queryset().filter(
            event__ends_at__gte=now,
            status='enrolled'
        ).order_by('event__starts_at')
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Enroll in an event."""
        event_id = request.data.get('event')
        if not event_id:
            return Response(
                {'detail': 'Event ID is required.', 'code': 'missing_event'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response(
                {'detail': 'Event not found.', 'code': 'event_not_found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if already enrolled
        existing = Enrollment.objects.filter(event=event, seeker=request.user).first()
        if existing:
            if existing.status == 'enrolled':
                return Response(
                    {'detail': 'You are already enrolled in this event.', 'code': 'already_enrolled'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # Re-enroll if previously canceled
                existing.status = 'enrolled'
                existing.save()
                
                # Schedule follow-up email
                from .tasks import send_followup_email
                send_followup_email.apply_async((existing.id,), countdown=3600)
                
                serializer = self.get_serializer(existing)
                return Response(serializer.data, status=status.HTTP_200_OK)

        # Check capacity
        if event.capacity is not None and event.available_seats <= 0:
            return Response(
                {'detail': 'Event is at full capacity.', 'code': 'capacity_full'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if event is past
        if event.is_past:
            return Response(
                {'detail': 'Cannot enroll in past events.', 'code': 'past_event'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data={'event': event_id, 'status': 'enrolled'})
        serializer.is_valid(raise_exception=True)
        serializer.save(seeker=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

