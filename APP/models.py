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

    def save(self, *args, **kwargs):
        # Check if the file exists in the filesystem before saving
        if self.pk:
            old_file = UploadedFile.objects.filter(pk=self.pk).first()
            if old_file and old_file.file != self.file and old_file.file.path:
                if os.path.exists(old_file.file.path):
                    os.remove(old_file.file.path)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem when the object is deleted
        if self.file and os.path.exists(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.file.name 