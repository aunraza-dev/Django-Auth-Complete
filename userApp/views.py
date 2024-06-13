from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from userApp.utils import verify_password, hash_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pyotp
from userApp.utils import Util
from django.contrib.auth import logout
from django.shortcuts import redirect, render

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email','username','password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'bio': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={200: 'Success', 400: 'Bad Request'},
    )
    def post(self, request, format=None):
        try:
            email = request.data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({'message': 'User with this email already exists.', 'success': False})

            password = request.data.get('password')
            totp = pyotp.TOTP(pyotp.random_base32(), digits=5)
            otp = totp.now()
            user = User.objects.create(
                email=email,
                username=request.data.get('username'),
                password=hash_password(password),
                otp=otp
            )

            email_data = {
                'subject': 'OTP for Registration',
                'body': f'Your OTP is: {otp}',
                'to_email': user.email
            }
            Util.send_email(email_data)
            
            return Response({'message': 'User Registered Successfully.', 'success': True})
        except Exception as e:
            return Response({'message': str(e), 'success': False})

class OtpVerifiedView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'otp'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'otp': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        responses={200: 'Success', 400: 'Bad Request'},
    )
    def post(self, request, format=None):
        try:
            email = request.data.get('email')
            otp = request.data.get('otp')

            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({'message': 'User with this email does not exist.', 'success': False})

            if user.otp != otp:
                return Response({'message': 'Incorrect OTP.', 'success': False})

            user.otpVerified = True
            user.save()

            return Response({'message': 'OTP verified successfully.', 'success': True})
        except Exception as e:
            return Response({'message': str(e), 'success': False})
                
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
        ),
        responses={200: 'Success', 400: 'Bad Request'},
    )
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            user = User.objects.filter(email=email).first()

            if user is None:
                return Response({'message': 'Email not found', 'success': False})

            if not verify_password(password, user.password):
                return Response({'message': 'The password you have entered is incorrect', 'success': False})


            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            userData = {
                'id': user.id,
                'email': user.email,
                'bio': user.bio
            }

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'data': userData,
                'message': 'User Login Success',
                'success': True
            })
        except Exception as e:
            return Response({'message': str(e), 'success': False})
        
class SendPasswordResetOtpView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={200: 'Success', 400: 'Bad Request'},
    )
    def post(self, request):
        try:
            email = request.data.get('email')
            user = User.objects.get(email=email)

            totp = pyotp.TOTP(pyotp.random_base32(), digits=5)
            otp = totp.now()

            email_data = {
                'subject': 'OTP for Password Reset',
                'body': f'Your OTP for Password Reset is: {otp}',
                'to_email': user.email
            }
            user.otp =otp
            user.save()
            Util.send_email(email_data)

            return Response({'message': 'Password Reset OTP sent successfully', 'success': True})
        except User.DoesNotExist:
            return Response({'message': 'User not found', 'success': False})
        except Exception as e:
            return Response({'message': str(e), 'success': False})

class PasswordResetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['new_password'],
            properties={
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
        ),
        responses={200: 'Success', 400: 'Bad Request'},
    )
    def post(self, request):
        try:
            new_password = request.data.get('new_password')
            hashed_password = hash_password(new_password)

            user = request.user
            user.password = hashed_password
            user.save()

            return Response({'message': 'Password updated successfully', 'success': True})
        except User.DoesNotExist:
            return Response({'message': 'User not found', 'success': False})
        except Exception as e:
            return Response({'message': str(e), 'success': False})
        
class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            responses={200:'Success', 400:'Bad Request'},
    )

    def get(self, request):
        try:
            user = request.user
            user_data = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'bio': user.bio
            }
            return Response({'data': user_data, 'message': 'User data retrieved successfully', 'success': True})
        except Exception as e:
            return Response({'message': str(e), 'success': False})
        
def logoutView(request):
    logout(request)
    return render(request, 'admin/logout.html')
