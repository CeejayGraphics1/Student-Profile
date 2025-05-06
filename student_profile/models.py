from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class AdminStaffManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)  # Set this to True
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('title', 'Mr')
        return self.create_user(email, password, **extra_fields)

class AdminStaff(AbstractUser):
    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Doctor', 'Doctor'),
        ('Amb', 'Ambassador'),
    ]
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]

    username = None  # Disable the username field
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='adminstaff_set',
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='adminstaff_set',
        help_text='Specific permissions for this user.'
    )

    objects = AdminStaffManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['title', 'role']

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True  # Automatically make admin users superusers
        super().save(*args, **kwargs)


class Student(models.Model):
    surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    level = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    matric_number = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.surname} {self.other_names} - {self.matric_number}"
