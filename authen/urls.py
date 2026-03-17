from django.urls import path
from .views import *

urlpatterns = [
    path('',login_,name='login_'),
    path('profile/',profile,name='profile'),
    path('register/',register,name='register'),
    path('logout_/',logout_,name='logout_'),
    path('update/',update,name='update'),
    path('reset/',reset,name='reset'),
    path('forgot_password/',forgot_password,name='forgot_password'),
]