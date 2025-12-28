from rest_framework import permissions
from .models import UserProfile


class IsVerified(permissions.BasePermission):
    """Check if user's email is verified."""
    message = "Please verify your email before accessing this resource."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'profile') and request.user.profile.is_email_verified


class IsSeeker(permissions.BasePermission):
    """Check if user is a Seeker."""
    message = "This resource is only accessible to Seekers."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'profile') and request.user.profile.role == 'Seeker'


class IsFacilitator(permissions.BasePermission):
    """Check if user is a Facilitator."""
    message = "This resource is only accessible to Facilitators."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'profile') and request.user.profile.role == 'Facilitator'


class IsEventOwner(permissions.BasePermission):
    """Check if user is the owner of the event."""
    message = "You do not have permission to perform this action on this event."

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user

