from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import signup, verify_email, user_profile, CustomTokenObtainPairView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('verify-email/', verify_email, name='verify-email'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', user_profile, name='user-profile'),
]

