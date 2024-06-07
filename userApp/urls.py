from django.urls import path
from userApp.views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', UserLoginView.as_view(), name='user_signin'),
    path('passwordReset/', PasswordResetView.as_view(), name='password_reset'),
]