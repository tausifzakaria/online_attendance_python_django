from django.urls import path
from .views import *
urlpatterns=[
    path('',home,name="home"),
    path('login',login,name="login"),
    path('logout',logout,name="logout"),
    path('register',register,name="register"),
    path('update_user',update_user,name="update_user"),
    path('delete',delete_user,name="delete"),
]