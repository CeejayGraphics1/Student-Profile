from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AdminStaffForm, ModifyMemberForm
from .models import AdminStaff, Student
from collections import defaultdict
from django.db.models import Q

from .forms import StudentForm

# Add a custom decorator to check if user is admin
def admin_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You must be logged in as an admin to access this page.")
            return redirect('login')
    return wrap

# Add a custom decorator to check if user is staff
def staff_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'staff':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You must be logged in as a staff to access this page.")
            return redirect('login')
    return wrap

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

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required
@admin_required
def dashboard(request):
    context = {
        'user': request.user
    }
    return render(request, 'dashboard.html', context)

@login_required
@admin_required
def view_students(request):
    selected_dept = request.GET.get('department', None)
    students_by_level = {}
    levels = [100, 200, 300]
    
    for level in levels:
        if selected_dept:
            students = Student.objects.filter(
                department__iexact=selected_dept.replace('_', ' '),
                level=str(level)
            )
        else:
            students = Student.objects.filter(level=str(level))
        students_by_level[level] = students.order_by('surname')
    
    context = {
        'students_by_level': students_by_level,
        'levels': levels,
        'selected_dept': selected_dept,
        'department_name': selected_dept.replace('_', ' ') if selected_dept else 'All Departments'
    }
    return render(request, 'view_student.html', context)

@login_required
@admin_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    
    if request.method == 'POST':
        # Perform the deletion
        student.delete()
        return redirect('view_students') 
    
    return HttpResponse("Method not allowed", status=405)

@login_required
@admin_required
def student_details(request, id):
    student = get_object_or_404(Student, pk=id)
    
    context = {
        'student': student,
    }
    return render(request, 'student_details.html', context)

@login_required
@admin_required
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

@login_required
@admin_required
def modify(request, id):
    student = get_object_or_404(Student, pk=id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student information updated successfully.")
            return redirect('student_details', id=student.id)
        else:
            messages.error(request, "Failed to update student. Please check the form.")
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'student': student
    }
    return render(request, 'modify.html', context)

@login_required
@admin_required
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

@login_required
@admin_required
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

@login_required
@admin_required
def view_admin(request):
    # Query for all admin and staff members
    admins = AdminStaff.objects.filter(role='admin')
    staff = AdminStaff.objects.filter(role='staff')
    
    context = {
        'admins': admins,
        'staff': staff,
    }
    return render(request, 'view-admin.html', context)

@login_required
@admin_required
def admin_details(request, id):
    # Fetch specific admin or staff member by ID
    admin_or_staff = get_object_or_404(AdminStaff, id=id)
    
    context = {
        'admin_or_staff': admin_or_staff,
    }
    
    return render(request, 'admin-details.html', context)

@login_required
@admin_required
def delete_admin_or_staff(request, id):
    # Fetch the admin or staff member by ID
    admin_or_staff = get_object_or_404(AdminStaff, id=id)
    
    if request.method == 'POST':
        # Perform the deletion
        admin_or_staff.delete()
        return redirect('view_admin')  # Redirect to the list page or a success page
    
    return HttpResponse("Method not allowed", status=405)

@login_required
@staff_required
def staff(request):
    return render(request, 'staff.html')

@login_required
@staff_required
def staff_view_students(request):
    # Add the same student grouping logic as in admin view
    students_by_level = {
        100: Student.objects.filter(level='100'),
        200: Student.objects.filter(level='200'),
        300: Student.objects.filter(level='300')
    }

    levels = [100, 200, 300]

    context = {
        'students_by_level': students_by_level,
        'levels': levels,
    }
    return render(request, 'staff-view-students.html', context)

@login_required
@staff_required
def staff_student_details(request, id):
    student = get_object_or_404(Student, pk=id)
    context = {
        'student': student,
    }
    return render(request, 'staff-student-details.html', context)

@login_required
@staff_required
def profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html', context)

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

def search_students(request):
    term = request.GET.get('term', '')
    if not term:
        return redirect('view_students')
    
    # Get all students matching the search term
    students = Student.objects.filter(
        Q(surname__icontains=term) |
        Q(other_names__icontains=term) |
        Q(matric_number__icontains=term) |
        Q(department__icontains=term) |
        Q(level__icontains=term)
    ).order_by('level', 'surname')
    
    # Group students by level as in view_students
    students_by_level = {}
    levels = [100, 200, 300]
    
    for level in levels:
        students_by_level[level] = students.filter(level=str(level))
    
    context = {
        'students_by_level': students_by_level,
        'levels': levels,
        'search_term': term,
        'is_search': True
    }
    
    return render(request, 'view_student.html', context)