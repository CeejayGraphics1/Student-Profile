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