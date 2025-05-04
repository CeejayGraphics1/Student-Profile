from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_students/', views.view_students, name='view_students'),
    path('student_details/', views.student_details, name='student_details'),
    path('upload/', views.upload, name='upload'),
    path('modify/', views.modify, name='modify'),
]