from django.contrib import admin
from django.urls import path,include
from myapp import views

urlpatterns = [
    path('',views.index),
    path('notes/',views.notes),
    path('profile/',views.profile),
    path('about/',views.about),
    path('contact/',views.contact),
    path('login/',views.login,name='login'),
    path('signup/',views.signup),
    path('otpverify/',views.otpverify,name='otpverify'),
    path('userlogout/',views.userlogout),
]
