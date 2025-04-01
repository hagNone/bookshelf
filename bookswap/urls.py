from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, SendResetOTPView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('send-reset-otp/', SendResetOTPView.as_view(), name='send_reset_otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]
