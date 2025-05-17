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

from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.http import HttpResponse
from PIL import Image
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
                    return redirect('dashboard')
                else:
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
    levels = [100, 200, 300, 400]
    
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
            return redirect('modify', id=student.id)
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
    departments = [
        'SOCIOLOGY', 'ECONOMICS', 'POLITICAL SCIENCE', 'COMPUTER SCIENCE',
        'MASS COMMUNICATION', 'ACCOUNTING & FINANCE', 'PUBLIC ADMINISTRATION',
        'BUSSINESS ADMINSTRATION', 'HUMAN RESOURCE MANAGEMENT',
        'INTERNATIONAL RELATION & DIPLOMACY', 'ENVIRONMENTAL HEALTH MANAGEMENT',
        'COMMUNITY HEALTH MANAGEMENT', 'NURSING'
    ]
    context = {
        'user': request.user,
        'departments': departments
    }
    return render(request, 'staff.html', context)

@login_required
@staff_required
def staff_view_students(request):
    selected_dept = request.GET.get('department')
    
    students_by_level = {}
    levels = [100, 200, 300]
    
    for level in levels:
        # Build the query
        query = Q(level=str(level))
        if selected_dept:
            # Make the department search case-insensitive
            query &= Q(department__iexact=selected_dept)
        
        # Get students for this level and department
        students = Student.objects.filter(query).order_by('surname')
        students_by_level[level] = students

    context = {
        'levels': levels,
        'students_by_level': students_by_level,
        'selected_dept': selected_dept,
        'departments': [
            'SOCIOLOGY', 'ECONOMICS', 'POLITICAL SCIENCE', 'COMPUTER SCIENCE',
            'MASS COMMUNICATION', 'ACCOUNTING & FINANCE', 'PUBLIC ADMINISTRATION',
            'BUSSINESS ADMINSTRATION', 'HUMAN RESOURCE MANAGEMENT',
            'INTERNATIONAL RELATION & DIPLOMACY', 'ENVIRONMENTAL HEALTH MANAGEMENT',
            'COMMUNITY HEALTH MANAGEMENT', 'NURSING'
        ]
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
def staff_search_students(request):
    search_term = request.GET.get('term', '')
    if search_term:
        # Enhanced search query
        students = Student.objects.filter(
            Q(surname__icontains=search_term) |
            Q(other_names__icontains=search_term) |
            Q(matric_number__icontains=search_term) |
            Q(department__icontains=search_term) |
            Q(level__icontains=search_term)  # Added level search
        ).order_by('level', 'surname')

        students_by_level = {}
        levels = [100, 200, 300]
        
        for level in levels:
            students_by_level[level] = students.filter(level=str(level))

        context = {
            'levels': levels,
            'students_by_level': students_by_level,
            'is_search': True,
            'search_term': search_term,
            'departments': [
                'SOCIOLOGY', 'ECONOMICS', 'POLITICAL SCIENCE', 'COMPUTER SCIENCE',
                'MASS COMMUNICATION', 'ACCOUNTING & FINANCE', 'PUBLIC ADMINISTRATION',
                'BUSSINESS ADMINSTRATION', 'HUMAN RESOURCE MANAGEMENT',
                'INTERNATIONAL RELATION & DIPLOMACY', 'ENVIRONMENTAL HEALTH MANAGEMENT',
                'COMMUNITY HEALTH MANAGEMENT', 'NURSING'
            ]
        }
        return render(request, 'staff-view-students.html', context)
    
    return redirect('staff_view_students')

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
    levels = [100, 200, 300, 400]
    
    for level in levels:
        students_by_level[level] = students.filter(level=str(level))
    
    context = {
        'students_by_level': students_by_level,
        'levels': levels,
        'search_term': term,
        'is_search': True
    }
    
    return render(request, 'view_student.html', context)

def export_student_pdf(request, id):
    # Get student
    student = get_object_or_404(Student, pk=id)
    
    # Create response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.surname} {student.other_names} details.pdf"'
    
    # Create PDF object
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Add logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'Espam Logo.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, width/2 - 50, height - 150, width=100, height=100)
    
    # Add header text
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 180, "ESPAM FORMATION UNIVERSITY")
    
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, height - 200, "Address: Sacouba Anavie Campus, Porto-Novo, Republic of Benin.")
    p.drawCentredString(width/2, height - 220, "Phone: +22946436904, +2348035637035, +22956885802")
    p.drawCentredString(width/2, height - 240, "Email: espamformationunicampus2@gmail.com")
    
    # Add title
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 280, "STUDENT PROFILE REPORT")
    
    # Draw line under title
    p.line(50, height - 290, width - 50, height - 290)
    
    # Add student photo
    if student.photo:
        try:
            photo_path = student.photo.path
            p.drawImage(photo_path, 50, height - 450, width=120, height=120)
        except:
            pass  # Skip if photo can't be loaded
    
    # Add student details
    p.setFont("Helvetica-Bold", 12)
    start_y = height - 350
    details = [
        f"Surname: {student.surname}",
        f"Other Names: {student.other_names}",
        f"Matric Number: {student.matric_number}",
        f"Date of Birth: {student.date_of_birth}",
        f"Level: {student.level}",
        f"Department: {student.department}"
    ]
    
    for i, detail in enumerate(details):
        p.drawString(200, start_y - (i * 25), detail)
    
    # Add footer with standard Helvetica font
    p.setFont("Helvetica", 8)
    p.drawCentredString(width/2, 30, "All rights reserved by ESPAM FORMATION UNIVERSITY.")
    
    # Save PDF
    p.showPage()
    p.save()
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

def export_students_pdf(request):
    # Get selected student IDs from query parameter
    student_ids = request.GET.get('ids', '').split(',')
    students = Student.objects.filter(id__in=student_ids).order_by('level', 'surname')

    if not students:
        return HttpResponse("No students selected", status=400)

    # Create response object
    if len(students) == 1:
        student = students.first()
        filename = f"{student.surname} {student.other_names} details.pdf"
    else:
        filename = "selected_students.pdf"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create PDF object
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Add logo and header
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'Espam Logo.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, width/2 - 50, height - 150, width=100, height=100)

    # Add header text
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 180, "ESPAM FORMATION UNIVERSITY")

    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, height - 200, "Address: Sacouba Anavie Campus, Porto-Novo, Republic of Benin.")
    p.drawCentredString(width/2, height - 220, "Phone: +22946436904, +2348035637035, +22956885802")
    p.drawCentredString(width/2, height - 240, "Email: espamformationunicampus2@gmail.com")

    # Add title
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 280, "STUDENT PROFILES REPORT")

    # Initialize starting position
    y_position = height - 320

    # Loop through each student
    for student in students:
        if y_position < 150:
            p.showPage()
            y_position = height - 100

        if y_position < height - 320:
            p.line(50, y_position + 30, width - 50, y_position + 30)
            y_position -= 20

        if student.photo:
            try:
                photo_path = student.photo.path
                p.drawImage(photo_path, 50, y_position - 100, width=100, height=100)
            except:
                pass

        p.setFont("Helvetica-Bold", 12)
        details = [
            f"Surname: {student.surname}",
            f"Other Names: {student.other_names}",
            f"Matric Number: {student.matric_number}",
            f"Date of Birth: {student.date_of_birth}",
            f"Level: {student.level}",
            f"Department: {student.department}"
        ]

        for i, detail in enumerate(details):
            p.drawString(200, y_position - (i * 20), detail)

        y_position -= 150

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

@login_required
def filter_student(request, id):
    student = get_object_or_404(Student, pk=id)
    return render(request, 'filter_student.html', {'student': student})

def export_filtered_pdf(request, id):
    student = get_object_or_404(Student, pk=id)
    selected_fields = request.GET.get('fields', '').split(',')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.surname} {student.other_names} filtered details.pdf.pdf"'
    
    # Create PDF object
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Add header
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'Espam Logo.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, width/2 - 50, height - 150, width=100, height=100)
    
    # Add header text
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 180, "ESPAM FORMATION UNIVERSITY")
    
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, height - 200, "Address: Sacouba Anavie Campus, Porto-Novo, Republic of Benin.")
    p.drawCentredString(width/2, height - 220, "Phone: +22946436904, +2348035637035, +22956885802")
    p.drawCentredString(width/2, height - 240, "Email: espamformationunicampus2@gmail.com")
    
    # Draw line under header
    p.line(50, height - 290, width - 50, height - 290)
    
    # Add title
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 280, "STUDENT PROFILE REPORT")
    
    # Add student photo if selected
    start_y = height - 350
    if 'photo' in selected_fields and student.photo:
        try:
            photo_path = student.photo.path
            p.drawImage(photo_path, 50, height - 450, width=120, height=120)
        except:
            pass
    
    # Add selected student details
    p.setFont("Helvetica-Bold", 12)
    field_mapping = {
        'surname': ('Surname', student.surname),
        'other_names': ('Other Names', student.other_names),
        'date_of_birth': ('Date of Birth', student.date_of_birth),
        'level': ('Level', student.level),
        'department': ('Department', student.department),
        'matric_number': ('Matric Number', student.matric_number),
    }
    
    for i, field in enumerate(selected_fields):
        if field in field_mapping and field != 'photo':
            label, value = field_mapping[field]
            p.drawString(200, start_y - (i * 25), f"{label}: {value}")
    
    # Add footer
    p.setFont("Helvetica", 8)
    p.drawCentredString(width/2, 30, "All rights reserved by ESPAM FORMATION UNIVERSITY.")
    
    # Save PDF
    p.showPage()
    p.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response