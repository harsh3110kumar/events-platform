from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import secrets
from datetime import timedelta


class UserProfile(models.Model):
    """Extended user profile with role information."""
    ROLE_CHOICES = [
        ('Seeker', 'Seeker'),
        ('Facilitator', 'Facilitator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.role}"


class EmailOTP(models.Model):
    """Email OTP for verification."""
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'created_at']),
        ]

    def is_expired(self):
        """Check if OTP is expired (5 minutes)."""
        expiry_time = self.created_at + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        return timezone.now() > expiry_time

    def can_attempt(self):
        """Check if more attempts are allowed."""
        return self.attempts < settings.OTP_MAX_ATTEMPTS and not self.is_expired() and not self.is_used

    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP."""
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

    def __str__(self):
        return f"{self.email} - {self.otp}"

