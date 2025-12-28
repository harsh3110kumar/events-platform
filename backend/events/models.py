from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Event(models.Model):
    """Event model."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    capacity = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['starts_at']
        indexes = [
            models.Index(fields=['starts_at']),
            models.Index(fields=['language']),
            models.Index(fields=['location']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.title} - {self.location}"

    @property
    def available_seats(self):
        """Calculate available seats."""
        if self.capacity is None:
            return None
        enrolled_count = self.enrollments.filter(status='enrolled').count()
        return max(0, self.capacity - enrolled_count)

    @property
    def total_enrollments(self):
        """Get total enrollments count."""
        return self.enrollments.filter(status='enrolled').count()

    @property
    def is_past(self):
        """Check if event has ended."""
        from django.utils import timezone
        return self.ends_at < timezone.now()


class Enrollment(models.Model):
    """Enrollment model."""
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('canceled', 'Canceled'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='enrollments')
    seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['event', 'seeker']]
        indexes = [
            models.Index(fields=['event', 'seeker']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.seeker.email} - {self.event.title} - {self.status}"

