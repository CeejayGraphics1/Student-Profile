from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AdminStaffForm, ModifyMemberForm
from .models import AdminStaff, Student
from collections import defaultdict

from .forms import StudentForm

def home(request):
    return render(request, 'index.html')    

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    messages.success(request, f'Welcome {user.title} {user.first_name}!')
                    return redirect('dashboard')
                else:
                    messages.success(request, f'Welcome {user.title} {user.first_name}!')
                    return redirect('staff')
            else:
                messages.error(request, 'Invalid email or password')
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

from .models import Student

def view_students(request):
    # Group students by level
    students_by_level = {
        100: Student.objects.filter(level='100'),
        200: Student.objects.filter(level='200'),
        300: Student.objects.filter(level='300')
    }

    levels = [100, 200, 300]  # Define the list of levels

    context = {
        'students_by_level': students_by_level,
        'levels': levels,  # Pass the levels list
    }

    return render(request, 'view_student.html', context)

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    
    if request.method == 'POST':
        # Perform the deletion
        student.delete()
        return redirect('view_students') 
    
    return HttpResponse("Method not allowed", status=405)

def student_details(request, id):
    student = get_object_or_404(Student, pk=id)
    
    context = {
        'student': student,
    }
    return render(request, 'student_details.html', context)

def upload(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Student uploaded successfully.")
            return redirect('upload')
        else:
            messages.error(request, "Failed to upload student. Please check the form.")
    else:
        form = StudentForm()
    return render(request, 'upload.html', {'form': form})

def modify(request):
    return render(request, 'modify.html')

def upload_admin(request):
    if request.method == 'POST':
        form = AdminStaffForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.username = form.cleaned_data['email']
                if form.cleaned_data['role'] == 'admin':
                    user.is_staff = True  # Give admin access to Django admin site
                user.save()
                messages.success(request, f"{user.get_role_display()} added successfully!")
                return redirect('upload_admin')
            except Exception as e:
                messages.error(request, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AdminStaffForm()
    
    return render(request, 'add-admin.html', {'form': form})

def modify_admin(request, id):
    admin_or_staff = get_object_or_404(AdminStaff, id=id)
    
    if request.method == 'POST':
        # Update the admin/staff details with the new data from the form
        title = request.POST.get('title')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Optional, can be updated if provided
        role = request.POST.get('role')

        # Update the fields
        admin_or_staff.title = title
        admin_or_staff.first_name = first_name
        admin_or_staff.last_name = last_name
        admin_or_staff.email = email
        if password:
            admin_or_staff.set_password(password)  # Only set password if provided
        admin_or_staff.role = role
        
        # Save the updated object
        admin_or_staff.save()
        
        messages.success(request, 'Admin/Staff details updated successfully!')
        return redirect('modify_admin', id=admin_or_staff.id)

    # Render the page with the current data if GET request
    context = {
        'admin_or_staff': admin_or_staff,
    }
    return render(request, 'modify-admin.html', context)

def view_admin(request):
    # Query for all admin and staff members
    admins = AdminStaff.objects.filter(role='admin')
    staff = AdminStaff.objects.filter(role='staff')
    
    context = {
        'admins': admins,
        'staff': staff,
    }
    return render(request, 'view-admin.html', context)

def admin_details(request, id):
    # Fetch specific admin or staff member by ID
    admin_or_staff = get_object_or_404(AdminStaff, id=id)
    
    context = {
        'admin_or_staff': admin_or_staff,
    }
    
    return render(request, 'admin-details.html', context)

def delete_admin_or_staff(request, id):
    # Fetch the admin or staff member by ID
    admin_or_staff = get_object_or_404(AdminStaff, id=id)
    
    if request.method == 'POST':
        # Perform the deletion
        admin_or_staff.delete()
        return redirect('view_admin')  # Redirect to the list page or a success page
    
    return HttpResponse("Method not allowed", status=405)

def staff(request):
    return render(request, 'staff.html')

def staff_view_students(request):
    return render(request, 'staff-view-students.html')

def staff_student_details(request):
    return render(request, 'staff-student-details.html')

def profile(request):
    return render(request, 'profile.html')

@login_required
@permission_required('student_profile.can_modify_members', raise_exception=True)
def modify_member(request, member_id):
    member = get_object_or_404(AdminStaff, id=member_id)
    if request.method == 'POST':
        form = ModifyMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member details updated successfully!')
            return redirect('view_admin')
    else:
        form = ModifyMemberForm(instance=member)
    
    return render(request, 'modify_member.html', {'form': form, 'member': member})