from django.urls import path
<<<<<<< HEAD
from .views import RegisterView, VerifyOTPView , LoginView, Userprofile, Booklist, BookDetail #, SendResetOTPView, ResetPasswordView,SearchBooksAPIView,user_logout,post_request
=======
from .views import RegisterView, VerifyOTPView , LoginView, Userprofile,SearchBooksAPIView,BookDetailAPIView,user_logout#, SendResetOTPView, ResetPasswordView,SearchBooksAPIView,BookDetailAPIView,post_request
>>>>>>> 44f5a727ece0bab70cded9e87073c520f783fbee

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
#     path('send-reset-otp/', SendResetOTPView.as_view(), name='send_reset_otp'),
#     path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
<<<<<<< HEAD
#     path('search/', SearchBooksAPIView.as_view(), name='search-books-page'),
    path('book/<int:book_id>/', BookDetail.as_view(), name='book-detail-page'),
    path('profile/',Userprofile.as_view(),name='profile-page'),
    path('Book_list/',Booklist.as_view(),name='Book_list'),
#     path("logout/",user_logout,name="user-Logout"),
=======
    path('search/', SearchBooksAPIView.as_view(), name='search-books-page'),
    path('book/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail-page'),
    path('profile/',Userprofile.as_view(),name='profile-page'),
    path("logout/",user_logout,name="user-Logout"),
>>>>>>> 44f5a727ece0bab70cded9e87073c520f783fbee
#     path('upload_book/',post_request,name='upload_book')
]
