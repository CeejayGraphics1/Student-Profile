# filepath: c:\Users\EMMANUEL AYANLEYE\Emmy\WEBDESIGN\studentprofile\student_profile\apps.py
from django.apps import AppConfig

class StudentProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student_profile'

    def ready(self):
        import student_profile.signals