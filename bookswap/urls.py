from django.urls import path
from .views import RegisterView, VerifyOTPView , LoginView, Userprofile, Booklist, BookDetail, RequestBook,Requestreject,Requestaccept ,user_logout #, SendResetOTPView, ResetPasswordView,SearchBooksAPIView,post_request

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
#     path('send-reset-otp/', SendResetOTPView.as_view(), name='send_reset_otp'),
#     path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
#     path('search/', SearchBooksAPIView.as_view(), name='search-books-page'),
    path('book/<int:book_id>/', BookDetail.as_view(), name='book-detail-page'),
    path('profile/',Userprofile.as_view(),name='profile-page'),
    path('Book_list/',Booklist.as_view(),name='Book_list'),
    path('request/book/<int:book_id>/',RequestBook.as_view(),name='Request_Book'),
    path('profile/accept/<int:request_id>/',Requestaccept.as_view(),name="Request_Accept"),
    path('profile/reject/<int:request_id>/',Requestaccept.as_view(),name="Request_Reject")
#     path("logout/",user_logout,name="user-Logout"),
#     path('upload_book/',post_request,name='upload_book')
]
