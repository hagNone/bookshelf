from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, SendResetOTPView, ResetPasswordView,SearchBooksAPIView,BookDetailAPIView,Userprofile,user_logout

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('send-reset-otp/', SendResetOTPView.as_view(), name='send_reset_otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('search/', SearchBooksAPIView.as_view(), name='search-books-page'),
    path('book/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail-page'),
    path('profile/',Userprofile.as_view(),name='profile-page'),
    path("logout/",user_logout,name="user-Logout"),
]
