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