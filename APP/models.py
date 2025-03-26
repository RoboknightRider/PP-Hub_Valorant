from django.db import models
from django.contrib.auth.models import User
import os

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    std_id = models.CharField(max_length=9, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
    
class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to="uploads/")  # Files will be saved in MEDIA_ROOT/uploads/
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"