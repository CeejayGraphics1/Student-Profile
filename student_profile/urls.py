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
    path('upload_admin/', views.upload_admin, name='upload_admin'),
    path('modify_admin/', views.modify_admin, name='modify_admin'),
    path('view_admin/', views.view_admin, name='view_admin'),
    path('admin_details/', views.admin_details, name='admin_details'),
    path('staff/', views.staff, name='staff'),
    path('staff_view_students/', views.staff_view_students, name='staff_view_students'),
    path('staff_student_details/', views.staff_student_details, name='staff_student_details'),
    path('profile/', views.profile, name='profile'),
]
