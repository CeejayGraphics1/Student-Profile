from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')    

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'password':  # Dummy check
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def view_students(request):
    return render(request, 'view_student.html')

def student_details(request):
    return render(request, 'student_details.html')

def upload(request):
    return render(request, 'upload.html')

def modify(request):
    return render(request, 'modify.html')

def upload_admin(request):
    return render(request, 'add-admin.html')

def modify_admin(request):
    return render(request, 'modify-admin.html')

def view_admin(request):
    return render(request, 'view-admin.html')

def admin_details(request):
    return render(request, 'admin-details.html')

def staff(request):
    return render(request, 'staff.html')

def staff_view_students(request):
    return render(request, 'staff-view-students.html')

def staff_student_details(request):
    return render(request, 'staff-student-details.html')

def profile(request):
    return render(request, 'profile.html')