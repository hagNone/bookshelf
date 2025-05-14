from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
#from .serializers import UserSerializer
from django.conf import settings
import random
import unicodedata
import re
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from bookswap.forms import Book_Model_Form
from bookswap.models import Book,Request


def generate_otp():
    return str(random.randint(100000, 999999))


def clean_text(text):
    """Remove non-breaking spaces and normalize the text to ASCII."""
    text = text.replace("\xa0", " ")  
    text = unicodedata.normalize("NFKD", text) 
    text = text.encode("ascii", "ignore").decode("utf-8")  
    text = re.sub(r'[^\x00-\x7F]+', '', text) 
    return text.strip()

##################################################################
# ======================== REGISTER ========================
# class RegisterView(APIView):
#     def get(self, request):
#         return render(request, 'register.html')

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)

#     # Check if email already exists
#         email = request.data.get('email')
#         if User.objects.filter(email=email).exists():
#             return Response({'error': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

#         if serializer.is_valid():
#             otp = generate_otp()
#             request.session['otp'] = otp
#             request.session['email'] = serializer.validated_data['email']

#             otp_message = clean_text(f'Your OTP is: {otp}')
#             try:
#                 send_mail(
#                 'Your OTP for Verification',
#                 otp_message,
#                 settings.EMAIL_HOST_USER,
#                 [serializer.validated_data['email']],
#                 fail_silently=False,
#             )
#             except Exception as e:
#                 return Response({'error': f'Failed to send email: {str(e)}'}, status=500)

#             return Response({'message': 'OTP sent. Verify your account.'}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# # ======================== VERIFY OTP ========================
# class VerifyOTPView(APIView):
#     def get(self, request):
#         return render(request, 'verify_otp.html')

#     def post(self, request):
#         entered_otp = request.data.get('otp')
#         username = request.data.get('username')
#         password = request.data.get('password')

#         stored_otp = request.session.get('otp')
#         email = request.session.get('email')

#         if not stored_otp or entered_otp != stored_otp:
#             return Response({"error": "Invalid OTP or session expired"}, status=400)

#         if not username:
#             return Response({"error": "Username is required!"}, status=400)

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

#         del request.session['otp']
#         del request.session['email']

#         return Response({"message": "User created successfully!"}, status=201)


# # ======================== LOGIN ========================
# class LoginView(APIView):
#     def get(self, request):
#         return render(request, 'login.html')

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user:
#             login(request, user)
#             return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# # ======================== SEND RESET OTP ========================
# class SendResetOTPView(APIView):
#     def get(self, request):
#         return render(request, 'send_reset_otp.html')

#     def post(self, request):
#         email = request.data.get('email')
#         try:
#             user = User.objects.get(email=email)
#             otp = generate_otp()
#             request.session['otp'] = otp
#             request.session['email'] = email

#             otp_message = clean_text(f'Your OTP is: {otp}')
#             try:
#                 send_mail(
#                     'Password Reset OTP',
#                     otp_message,
#                     settings.EMAIL_HOST_USER,
#                     [email],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 return Response({'error': f'Failed to send email: {str(e)}'}, status=500)

#             return Response({'message': 'OTP sent for password reset.'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# # ======================== RESET PASSWORD ========================
# class ResetPasswordView(APIView):
#     def get(self, request):
#         step = request.GET.get("step")

#         if step == "send_otp":
#             email = request.GET.get("email")
#             try:
#                 user = User.objects.get(email=email)
#                 otp = generate_otp()
#                 request.session['otp'] = otp
#                 request.session['email'] = email

#                 otp_message = clean_text(f'Your OTP is: {otp}')
#                 try:
#                     send_mail(
#                         'Password Reset OTP',
#                         otp_message,
#                         settings.EMAIL_HOST_USER,
#                         [email],
#                         fail_silently=False,
#                     )
#                 except Exception as e:
#                     return Response({'error': f'Failed to send email: {str(e)}'}, status=500)

#                 return Response({"message": "OTP sent!"})
#             except User.DoesNotExist:
#                 return Response({"error": "User not found"}, status=404)

#         elif step == "verify_otp":
#             entered_otp = request.GET.get("otp")
#             stored_otp = request.session.get("otp")
#             if not stored_otp or entered_otp != stored_otp:
#                 return Response({"error": "Invalid OTP or session expired"}, status=400)
#             return Response({"message": "OTP verified!"})

#         elif step == "reset_password":
#             new_password = request.GET.get("new_password")
#             email = request.session.get("email")
#             if email:
#                 user = User.objects.get(email=email)
#                 user.set_password(new_password)
#                 user.save()

#                 del request.session['otp']
#                 del request.session['email']

#                 return Response({"message": "Password reset successful!"})
#             return Response({"error": "Session expired"}, status=400)

#         return render(request, 'reset_password.html')

# from rest_framework.views import APIView
# from django.shortcuts import render, get_object_or_404
# from .models import FactBookListing

# @method_decorator(login_required, name='dispatch')
# class SearchBooksAPIView(APIView):
#     def get(self, request):
#         query = request.GET.get('q', '')
#         books = []
#         if query:
#             listings = FactBookListing.objects.filter(
#                 book__book_name__icontains=query
#             ).select_related('book', 'user', 'book__genre')
#             books = [
#                 {'id': listing.id, 'book_name': listing.book.book_name}
#                 for listing in listings
#             ]
#         return render(request, 'search.html', {'books': books, 'query': query})

# @method_decorator(login_required, name='dispatch')
# class BookDetailAPIView(APIView):
#     def get(self, request, pk):
#         listing = get_object_or_404(
#             FactBookListing.objects.select_related('book', 'user', 'book__genre'),
#             pk=pk
#         )
#         book = {
#             'book_name': listing.book.book_name,
#             'genre': listing.book.genre.genre_name,
#             'username': listing.user.username
#         }
#         return render(request, 'book_detail.html', {'book': book})

# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views import View
# from django.shortcuts import render
# from .models import FactBookListing, FactGenre, FactRequest, Book
# from .forms import Book_Model_Form

# @method_decorator(login_required, name='dispatch')
# class Userprofile(View):
#     def get(self, request):
#         user = request.user
#         books = FactBookListing.objects.filter(user=user)
#         genres = FactGenre.objects.filter(user=user)
#         sent_requests = FactRequest.objects.filter(requester=user)
#         received_requests = FactRequest.objects.filter(receiver=user)

#         context = {
#             'user': user,
#             'books': books,
#             'genres': genres,
#             'sent_requests': sent_requests,
#             'received_requests': received_requests,
#         }

#         return render(request, 'profile.html', context)

# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect("login")


# @login_required
# def post_request(request):

#     if request.method == 'POST':
#         form = Book_Model_Form(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('search-books-page')
#     else:
#         form = Book_Model_Form()
#         return render(request,'post_request.html',{'form':form})


###############################################################################



#                   Register                #


class RegisterView(View):
    def get(self, request):
            return render(request, 'register.html')
        
    def post(self,request):
        try:    
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            otp = generate_otp()
            request.session["otp"] = otp
            request.session["username"] = username
            request.session["email"] = email
            request.session["password"] = password

            send_mail(
                'Your OTP for Verification',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return redirect('verify_otp')
        except Exception as e:
            print(f"Error in registration: {e}")




#                   Verify Otp                #


class VerifyOTPView(View):
    def get(self,request):
        return render(request, "verify_otp.html")
    
    def post(self,request):
        try:
            OTP = request.POST.get("otp")
            Stored_OTP = request.session.get("otp")

            if OTP == Stored_OTP:
                if User.objects.filter(username=request.session.get("username")).exists():
                    return render(request, "verify_otp.html", {'error':"Username already Exists"})
                else:    
                    user = User.objects.create_user(username=request.session.get("username"), email=request.session.get("email"), password=request.session.get("password"))
                    
                    request.session.pop('otp', None)
                    request.session.pop('email', None)
                    request.session.pop('username', None)
                    request.session.pop('password', None)

                    return redirect('login')
                    #return HttpResponse("Logged In!!")
                    
            else:
                    return render(request, "verify_otp.html", {'error':"Invalid OTP"})
        except Exception as e:
            print(f"Error in registration: {e}")



#                   Login                #

class LoginView(View):
    def get(self,request):
         return render(request,"login.html")
    
    def post(self,request):
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")

            current_User = authenticate(request=request,username=username,password=password)

            # if User.objects.filter(username=username).exists():
            #     current_User =  User.objects.filter(username=username)

            if current_User is not None:     #password == current_User.values("password"):
                    login(request, current_User)
                    return redirect('profile-page')
                    #return HttpResponse("Profile !!")
                
            else:
                    return HttpResponse("Password Invalid !! Reset Password in case forgot !")
            
            # else:
            #     return HttpResponse("Username already exist !!")
        except Exception as e:
                    print(f"Error in registration: {e}")




#                   User Profile                #


@method_decorator(login_required, name='dispatch')
class Userprofile(View):
    try:
        def get(self,request):
            Current_user_info = User.objects.get(id=request.user.id)
            book_list_form = Book_Model_Form()
            Book_List = Book.objects.filter(user=request.user)

            context = {'username':Current_user_info.username,'email':Current_user_info.email,'date_joined':Current_user_info.date_joined,'book_list_form':book_list_form,'Book_List':Book_List}
            return render(request,'profile.html',context=context)
        
        def post(self,request):
            form = Book_Model_Form(request.POST)
            if form.is_valid():
                Submitted_Form = form.save(commit=False)
                Submitted_Form.user = request.user
                Submitted_Form.save()
                print("Form saved successfully")
                return redirect('profile-page')
            else:
                Current_user_info = User.objects.get(id=request.user.id)
                book_list_form = Book_Model_Form()
                Book_List = Book.objects.filter(user=request.user)
                context = {'username':Current_user_info.username,'email':Current_user_info.email,'date_joined':Current_user_info.date_joined,'book_list_form':book_list_form,'Book_List':Book_List,'error':'Form entry is invalid! please enter again.'}
                return render(request,'profile.html',context=context)

    except Exception as e:
                    print(f"Error in registration: {e}")



@method_decorator(login_required, name='dispatch')
class Booklist(View):
    def get(self,request):
        try:
            bookAllList = Book.objects.exclude(user=request.user)
            return render(request,'Book_list.html',{'books':bookAllList})
        except Exception as e:
                    print(f"Error in registration: {e}")

    def post(self,request):
        pass


@method_decorator(login_required, name='dispatch')
class BookDetail(View):
     def get(self,request,book_id):
        try:
             book_detail = get_object_or_404(Book, book_id=book_id)
             return render(request,"Book_detail.html",{'book':book_detail})
        except Exception as e:
                    print(f"Error in registration: {e}")
