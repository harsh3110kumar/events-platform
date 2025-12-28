from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, EmailOTP
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class SignupSerializer(serializers.Serializer):
    """Serializer for user signup."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    def validate_email(self, value):
        """Check if email already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """Create user and send OTP."""
        email = validated_data['email']
        password = validated_data['password']
        role = validated_data['role']

        # Create user with email as username (temporary, won't be used)
        user = User.objects.create_user(
            username=email,  # Django requires username, but we'll use email for auth
            email=email,
            password=password,
            is_active=True  # Active but unverified
        )

        # Create profile
        profile = UserProfile.objects.create(user=user, role=role, is_email_verified=False)

        # Generate and send OTP
        otp = EmailOTP.generate_otp()
        EmailOTP.objects.create(email=email, otp=otp)

        # Send OTP email (in production, use proper email service)
        try:
            send_mail(
                subject='Verify your email - Events Platform',
                message=f'Your OTP is: {otp}. It will expire in {settings.OTP_EXPIRY_MINUTES} minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            # Log error in production
            print(f"Error sending email: {e}")

        return user


class VerifyEmailSerializer(serializers.Serializer):
    """Serializer for email verification."""
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        """Validate OTP."""
        email = attrs['email']
        otp = attrs['otp']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist."})

        # Get the most recent valid OTP
        otp_obj = EmailOTP.objects.filter(
            email=email,
            is_used=False
        ).order_by('-created_at').first()

        if not otp_obj:
            raise serializers.ValidationError({"otp": "No valid OTP found. Please request a new one."})

        if otp_obj.is_expired():
            raise serializers.ValidationError({"otp": "OTP has expired. Please request a new one."})

        if not otp_obj.can_attempt():
            raise serializers.ValidationError({"otp": "Maximum attempts exceeded. Please request a new OTP."})

        if otp_obj.otp != otp:
            otp_obj.attempts += 1
            otp_obj.save()
            remaining = settings.OTP_MAX_ATTEMPTS - otp_obj.attempts
            if remaining > 0:
                raise serializers.ValidationError({"otp": f"Invalid OTP. {remaining} attempts remaining."})
            else:
                raise serializers.ValidationError({"otp": "Maximum attempts exceeded. Please request a new OTP."})

        attrs['otp_obj'] = otp_obj
        attrs['user'] = user
        return attrs

    def verify(self):
        """Mark email as verified."""
        otp_obj = self.validated_data['otp_obj']
        user = self.validated_data['user']

        otp_obj.is_used = True
        otp_obj.save()

        profile = user.profile
        profile.is_email_verified = True
        profile.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user information."""
    role = serializers.CharField(source='profile.role', read_only=True)
    is_email_verified = serializers.BooleanField(source='profile.is_email_verified', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'is_email_verified', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined')

