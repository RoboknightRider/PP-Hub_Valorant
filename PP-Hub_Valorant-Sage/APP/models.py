from django.db import models
from django.contrib.auth.models import User
import os

# StudentProfile model: Stores extra information about the user (Student Profile)
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    std_id = models.CharField(max_length=9, unique=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

# UploadedFile model: Stores information about the files uploaded by users
class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to="uploads/")  # Files will be saved in MEDIA_ROOT/uploads/
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seed_count = models.IntegerField(default=1)  # Default seed count is 1

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

# ChatMessage model: Stores messages sent by users in the chat system
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"

# DownloadHistory model: Tracks the files downloaded by users
class DownloadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the download time

    def __str__(self):
        return f"{self.user.username} downloaded {self.file.name} on {self.downloaded_at}"
