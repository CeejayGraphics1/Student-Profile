from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import AdminStaff

@receiver(post_save, sender=AdminStaff)
def set_admin_permissions(sender, instance, created, **kwargs):
    if instance.role == 'admin':
        content_type = ContentType.objects.get_for_model(AdminStaff)
        permission, created = Permission.objects.get_or_create(
            content_type=content_type,
            codename='can_modify_members',
            defaults={'name': 'Can modify member details'}
        )
        if not instance.user_permissions.filter(id=permission.id).exists():
            instance.user_permissions.add(permission)
