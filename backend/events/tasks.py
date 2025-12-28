from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import Enrollment, Event


@shared_task
def send_followup_email(enrollment_id):
    """Send follow-up email to seeker 1 hour after enrollment."""
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id, status='enrolled')
        event = enrollment.event
        seeker = enrollment.seeker

        subject = f'Thank you for enrolling in {event.title}'
        message = f"""
Hello {seeker.email},

Thank you for enrolling in "{event.title}"!

Event Details:
- Location: {event.location}
- Starts: {event.starts_at.strftime('%Y-%m-%d %H:%M UTC')}
- Language: {event.language}

We look forward to seeing you there!

Best regards,
Events Platform Team
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seeker.email],
            fail_silently=False,
        )
    except Enrollment.DoesNotExist:
        pass


@shared_task
def send_reminder_emails():
    """Send reminder emails to seekers 1 hour before their enrolled events start."""
    now = timezone.now()
    reminder_time = now + timedelta(hours=1)
    reminder_window_end = reminder_time + timedelta(minutes=5)  # 5-minute window

    # Get enrollments for events starting in approximately 1 hour
    enrollments = Enrollment.objects.filter(
        status='enrolled',
        event__starts_at__gte=reminder_time,
        event__starts_at__lte=reminder_window_end,
    ).select_related('event', 'seeker')

    for enrollment in enrollments:
        event = enrollment.event
        seeker = enrollment.seeker

        subject = f'Reminder: {event.title} starts in 1 hour!'
        message = f"""
Hello {seeker.email},

This is a reminder that "{event.title}" starts in 1 hour!

Event Details:
- Location: {event.location}
- Starts: {event.starts_at.strftime('%Y-%m-%d %H:%M UTC')}
- Language: {event.language}

See you soon!

Best regards,
Events Platform Team
        """

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[seeker.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log error in production
            print(f"Error sending reminder email to {seeker.email}: {e}")

