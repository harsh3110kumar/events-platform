from django.contrib import admin
from .models import UserProfile, EmailOTP


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_email_verified', 'created_at']
    list_filter = ['role', 'is_email_verified']
    search_fields = ['user__email']


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp', 'created_at', 'attempts', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['email']

