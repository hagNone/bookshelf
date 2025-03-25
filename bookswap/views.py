from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.conf import settings
import random
from django.http import JsonResponse

def generate_otp():
    return str(random.randint(100000, 999999))


@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        otp = generate_otp()
        request.session['otp'] = otp
        request.session['email'] = serializer.validated_data['email']

        send_mail(
            'Your OTP for Verification',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [serializer.validated_data['email']],
            fail_silently=False,
        )
        return Response({'message': 'OTP sent. Verify your account.'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def verify_otp(request):
    if request.method == 'GET':
        return render(request, 'verify_otp.html')

    entered_otp = request.data.get('otp')
    username = request.data.get('username')
    password = request.data.get('password')

    stored_otp = request.session.get('otp')
    email = request.session.get('email')

    if entered_otp != stored_otp:
        return Response({"error": "Invalid OTP"}, status=400)

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


@api_view(['GET', 'POST'])
def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET', 'POST'])
def send_reset_otp(request):
    if request.method == 'GET':
        return render(request, 'send_reset_otp.html')

    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        otp = generate_otp()
        request.session['otp'] = otp
        request.session['email'] = email

        send_mail(
            'Password Reset OTP',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'OTP sent for password reset.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', 'POST'])
def reset_password(request):
    if request.method == "POST":
        step = request.POST.get("step")

        if step == "send_otp":
            email = request.POST.get("email")
            try:
                user = User.objects.get(email=email)
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['email'] = email

                send_mail(
                    'Password Reset OTP',
                    f'Your OTP is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return JsonResponse({"message": "OTP sent!"})
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

        elif step == "verify_otp":
            entered_otp = request.POST.get("otp")
            stored_otp = request.session.get("otp")
            if entered_otp == stored_otp:
                return JsonResponse({"message": "OTP verified!"})
            else:
                return JsonResponse({"error": "Invalid OTP"}, status=400)

        elif step == "reset_password":
            new_password = request.POST.get("new_password")
            email = request.session.get("email")
            if email:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()

                del request.session['otp']
                del request.session['email']

                return JsonResponse({"message": "Password reset successful!"})
            return JsonResponse({"error": "Session expired"}, status=400)

    return render(request, 'reset_password.html')
