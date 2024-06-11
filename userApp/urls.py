from django.urls import path
from userApp.views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('otpVerified/', OtpVerifiedView.as_view(), name='otp_verified'),
    path('login/', UserLoginView.as_view(), name='user_signin'),
    path('sendPasswordResetOtp/',SendPasswordResetOtpView.as_view(),name="sendPasswordResetOtp"),
    path('passwordReset/', PasswordResetView.as_view(), name='password_reset'),
    path('userDetail/', UserDetailView.as_view(), name='user_detail'),
]