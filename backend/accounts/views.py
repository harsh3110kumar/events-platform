from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UserProfile, EmailOTP
from .serializers import SignupSerializer, VerifyEmailSerializer, UserSerializer
from .permissions import IsVerified


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view that checks email verification."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'detail': 'Email and password are required.', 'code': 'missing_credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Invalid email or password.', 'code': 'invalid_credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Check if email is verified
        if not hasattr(user, 'profile') or not user.profile.is_email_verified:
            return Response(
                {'detail': 'Please verify your email before logging in.', 'code': 'email_not_verified'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Verify password
        if not user.check_password(password):
            return Response(
                {'detail': 'Invalid email or password.', 'code': 'invalid_credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Create unverified user and send OTP."""
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                'detail': 'User created successfully. Please verify your email with the OTP sent.',
                'code': 'signup_success'
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """Verify email with OTP."""
    serializer = VerifyEmailSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.verify()
        return Response(
            {
                'detail': 'Email verified successfully. You can now log in.',
                'code': 'email_verified'
            },
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsVerified])
def user_profile(request):
    """Get current user profile."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

