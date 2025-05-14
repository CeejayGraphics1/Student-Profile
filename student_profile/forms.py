from django import forms
from .models import AdminStaff

class AdminStaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    class Meta:
        model = AdminStaff
        fields = ['title', 'first_name', 'last_name', 'email', 'role', 'password']
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'role': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }

class ModifyMemberForm(forms.ModelForm):
    class Meta:
        model = AdminStaff
        fields = ['title', 'first_name', 'last_name', 'email', 'role']
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }


from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['surname', 'other_names', 'date_of_birth', 'level', 'department', 'matric_number', 'photo']

    def clean_matric_number(self):
        matric_number = self.cleaned_data.get('matric_number')
        # Check if matric number exists but exclude the current instance
        if Student.objects.filter(matric_number=matric_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Matric number already exists.")
        return matric_number
