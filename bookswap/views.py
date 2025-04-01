from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from django.conf import settings
import random
import unicodedata
import re


def generate_otp():
    return str(random.randint(100000, 999999))


def clean_text(text):
    """Remove non-breaking spaces and normalize the text to ASCII."""
    text = text.replace("\xa0", " ")  
    text = unicodedata.normalize("NFKD", text) 
    text = text.encode("ascii", "ignore").decode("utf-8")  
    text = re.sub(r'[^\x00-\x7F]+', '', text) 
    return text.strip()


# ======================== REGISTER ========================
class RegisterView(APIView):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        serializer = UserSerializer(data=request.data)

    # Check if email already exists
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = serializer.validated_data['email']

            otp_message = clean_text(f'Your OTP is: {otp}')
            try:
                send_mail(
                'Your OTP for Verification',
                otp_message,
                settings.EMAIL_HOST_USER,
                [serializer.validated_data['email']],
                fail_silently=False,
            )
            except Exception as e:
                return Response({'error': f'Failed to send email: {str(e)}'}, status=500)

            return Response({'message': 'OTP sent. Verify your account.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ======================== VERIFY OTP ========================
class VerifyOTPView(APIView):
    def get(self, request):
        return render(request, 'verify_otp.html')

    def post(self, request):
        entered_otp = request.data.get('otp')
        username = request.data.get('username')
        password = request.data.get('password')

        stored_otp = request.session.get('otp')
        email = request.session.get('email')

        if not stored_otp or entered_otp != stored_otp:
            return Response({"error": "Invalid OTP or session expired"}, status=400)

        if not username:
            return Response({"error": "Username is required!"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        del request.session['otp']
        del request.session['email']

        return Response({"message": "User created successfully!"}, status=201)


# ======================== LOGIN ========================
class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# ======================== SEND RESET OTP ========================
class SendResetOTPView(APIView):
    def get(self, request):
        return render(request, 'send_reset_otp.html')

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email

            otp_message = clean_text(f'Your OTP is: {otp}')
            try:
                send_mail(
                    'Password Reset OTP',
                    otp_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({'error': f'Failed to send email: {str(e)}'}, status=500)

            return Response({'message': 'OTP sent for password reset.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# ======================== RESET PASSWORD ========================
class ResetPasswordView(APIView):
    def get(self, request):
        step = request.GET.get("step")

        if step == "send_otp":
            email = request.GET.get("email")
            try:
                user = User.objects.get(email=email)
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['email'] = email

                otp_message = clean_text(f'Your OTP is: {otp}')
                try:
                    send_mail(
                        'Password Reset OTP',
                        otp_message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                except Exception as e:
                    return Response({'error': f'Failed to send email: {str(e)}'}, status=500)

                return Response({"message": "OTP sent!"})
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

        elif step == "verify_otp":
            entered_otp = request.GET.get("otp")
            stored_otp = request.session.get("otp")
            if not stored_otp or entered_otp != stored_otp:
                return Response({"error": "Invalid OTP or session expired"}, status=400)
            return Response({"message": "OTP verified!"})

        elif step == "reset_password":
            new_password = request.GET.get("new_password")
            email = request.session.get("email")
            if email:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()

                del request.session['otp']
                del request.session['email']

                return Response({"message": "Password reset successful!"})
            return Response({"error": "Session expired"}, status=400)

        return render(request, 'reset_password.html')
