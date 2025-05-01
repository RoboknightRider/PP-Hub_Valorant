from django.contrib import admin
from .models import StudentProfile, UploadedFile, ChatMessage

admin.site.register(StudentProfile)
admin.site.register(UploadedFile)
admin.site.register(ChatMessage)
