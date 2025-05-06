from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminStaff

class AdminStaffAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'title', 'role', 'is_active', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('title', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),  # include is_superuser
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'title', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except Exception as e:
            self.message_user(request, f"Error saving user: {str(e)}", level='ERROR')

    def delete_model(self, request, obj):
        try:
            obj.delete()
        except Exception as e:
            self.message_user(request, f"Error deleting user: {str(e)}", level='ERROR')

admin.site.register(AdminStaff, AdminStaffAdmin)
