from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AdminStaffForm, ModifyMemberForm
from .models import AdminStaff

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

def view_students(request):
    return render(request, 'view_student.html')

def student_details(request):
    return render(request, 'student_details.html')

def upload(request):
    return render(request, 'upload.html')

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

def modify_admin(request):
    return render(request, 'modify-admin.html')

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