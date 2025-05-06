from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_students/', views.view_students, name='view_students'),
    path('student_details/', views.student_details, name='student_details'),
    path('upload/', views.upload, name='upload'),
    path('modify/', views.modify, name='modify'),
    path('upload_admin/', views.upload_admin, name='upload_admin'),
    path('modify_admin/', views.modify_admin, name='modify_admin'),
    path('admin_details/<int:id>/', views.admin_details, name='admin_details'),
    path('delete_admin_or_staff/<int:id>/', views.delete_admin_or_staff, name='delete_admin_or_staff'),
    path('view_admin/', views.view_admin, name='view_admin'),
    path('staff/', views.staff, name='staff'),
    path('staff_view_students/', views.staff_view_students, name='staff_view_students'),
    path('staff_student_details/', views.staff_student_details, name='staff_student_details'),
    path('profile/', views.profile, name='profile'),
]
