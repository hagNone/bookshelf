from django.urls import path
from .views import register, verify_otp, login_user, send_reset_otp, reset_password

urlpatterns = [
    path('register/', register, name='register'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('login/', login_user, name='login'),
    path('send-reset-otp/', send_reset_otp, name='send_reset_otp'),
    path('reset-password/', reset_password, name='reset_password'),
]
