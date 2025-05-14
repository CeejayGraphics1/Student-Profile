from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_students/', views.view_students, name='view_students'),
    path('student_details/<int:id>/', views.student_details, name='student_details'),
    path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('upload/', views.upload, name='upload'),
    path('modify/<int:id>/', views.modify, name='modify'),
    path('upload_admin/', views.upload_admin, name='upload_admin'),
    path('modify_admin/<int:id>/', views.modify_admin, name='modify_admin'),
    path('admin_details/<int:id>/', views.admin_details, name='admin_details'),
    path('delete_admin_or_staff/<int:id>/', views.delete_admin_or_staff, name='delete_admin_or_staff'),
    path('view_admin/', views.view_admin, name='view_admin'),
    path('staff/dashboard/', views.staff, name='staff'),
    path('staff/view-students/', views.staff_view_students, name='staff_view_students'),
    path('staff/view-student/details/<int:id>/', views.staff_student_details, name='staff_student_details'),
    path('staff/profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('modify_member/<int:member_id>/', views.modify_member, name='modify_member'),
    path('search/', views.search_students, name='search_students'),
    path('export_student_pdf/<int:id>/', views.export_student_pdf, name='export_student_pdf'),
    path('export_students_pdf/', views.export_students_pdf, name='export_students_pdf'),
    path('filter_student/<int:id>/', views.filter_student, name='filter_student'),
    path('export_filtered_pdf/<int:id>/', views.export_filtered_pdf, name='export_filtered_pdf'),
    path('staff/search/', views.staff_search_students, name='staff_search_students'),
]
