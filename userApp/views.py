from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from userApp.utils import verify_password, hash_password

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            email = request.data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({'message': 'User with this email already exists.', 'success': False})

            password = request.data.get('password')
            user = User.objects.create(
                email=email,
                username=request.data.get('username'),
                password=hash_password(password),
            )
            return Response({'message': 'User Registered Successfully.', 'success': True})
        except Exception as e:
            return Response({'message': str(e), 'success': False})
        
class UserLoginView(APIView):
    permission_classes = [AllowAny]

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
        
class PasswordResetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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