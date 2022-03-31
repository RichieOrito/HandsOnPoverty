from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcome, name="main"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout")
]
