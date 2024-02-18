from . import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('',views.index, name='index'),
    path('home/', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout, name='logout'),
    
   
]