from rest_framework import serializers
from .models import Event, Enrollment
from django.utils import timezone
from django.core.exceptions import ValidationError


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    available_seats = serializers.SerializerMethodField()
    total_enrollments = serializers.IntegerField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    
    def get_available_seats(self, obj):
        """Get available seats."""
        return obj.available_seats

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'language', 'location',
            'starts_at', 'ends_at', 'capacity', 'created_by',
            'created_by_email', 'available_seats', 'total_enrollments',
            'is_past', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate event data."""
        starts_at = attrs.get('starts_at')
        ends_at = attrs.get('ends_at')

        if starts_at and ends_at:
            if ends_at <= starts_at:
                raise serializers.ValidationError("End time must be after start time.")

            if starts_at < timezone.now():
                raise serializers.ValidationError("Start time cannot be in the past.")

        return attrs


class EventListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for event lists."""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    available_seats = serializers.SerializerMethodField()
    total_enrollments = serializers.IntegerField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    
    def get_available_seats(self, obj):
        """Get available seats."""
        return obj.available_seats

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'language', 'location',
            'starts_at', 'ends_at', 'capacity', 'created_by_email',
            'available_seats', 'total_enrollments', 'is_past'
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model."""
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_starts_at = serializers.DateTimeField(source='event.starts_at', read_only=True)
    event_location = serializers.CharField(source='event.location', read_only=True)
    seeker_email = serializers.EmailField(source='seeker.email', read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'event', 'event_title', 'event_starts_at', 'event_location',
            'seeker', 'seeker_email', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['seeker', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate enrollment."""
        event = attrs.get('event') or self.instance.event if self.instance else None
        if not event:
            event = self.context.get('event')

        if event and event.is_past:
            raise serializers.ValidationError("Cannot enroll in past events.")

        if attrs.get('status') == 'enrolled' and event:
            # Check capacity
            if event.capacity is not None:
                available = event.available_seats
                if available <= 0:
                    raise serializers.ValidationError("Event is at full capacity.")

        return attrs

