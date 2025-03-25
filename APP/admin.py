from django.contrib import admin
from .models import StudentProfile, UploadedFile

admin.site.register(StudentProfile)
admin.site.register(UploadedFile)