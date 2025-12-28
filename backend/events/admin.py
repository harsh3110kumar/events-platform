from django.contrib import admin
from .models import Event, Enrollment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'language', 'starts_at', 'created_by', 'total_enrollments', 'capacity']
    list_filter = ['language', 'location', 'starts_at']
    search_fields = ['title', 'description', 'location']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['event', 'seeker', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['event__title', 'seeker__email']

