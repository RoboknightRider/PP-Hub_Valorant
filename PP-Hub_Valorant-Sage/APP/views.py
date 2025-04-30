from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, UploadedFile, ChatMessage, DownloadHistory
import os, json
from django.http import JsonResponse

# Home view
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        profile = StudentProfile.objects.get(user=request.user)
        latest_files = UploadedFile.objects.order_by('-uploaded_at')[:10]
        return render(request, 'home2.html', {"profile": profile, "latest_files": latest_files})

# Registration view
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        std_id = request.POST.get("id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        # Validation: Check if any field is empty
        if not all([name, std_id, email, password, confirm_password]):
            messages.error(request, "All fields are required")
            return redirect("register")

        if email.find("@ulab.edu.bd") == -1:
            messages.error(request, "Please use your ULAB email")
            return redirect("register")

        if len(password) < 3:
            messages.error(request, "Password must be at least 3 characters long")
            return redirect("register")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Password do not match")
            return redirect("register")

        # Check if user already exists (by ID or email)
        if StudentProfile.objects.filter(std_id=std_id).exists():
            messages.error(request, "User with this ID already exists")
            return redirect("register")

        if User.objects.filter(username=name).exists():
            messages.error(request, "User with this username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists")
            return redirect("register")

        # Create the user and student profile
        user = User.objects.create_user(username=name, email=email, password=password)
        StudentProfile.objects.create(user=user, std_id=std_id)

        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")

    return render(request, "register.html", {"csrf_token": get_token(request)})

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html', {"csrf_token": get_token(request)})

# Logout view
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

# Upload view
@login_required
def upload(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        file = request.FILES.get("file")  # This handles file upload
        thumbnail = request.FILES.get("thumbnail")  # Handle thumbnail upload
        user = request.user

        # Check if a file is provided
        if not file:
            messages.error(request, "No file provided. Please upload a file.")
            return redirect("upload")

        # Process file type
        file_extension = os.path.splitext(file.name)[1].lower()
        file_type = file_extension[1:] if file_extension.startswith(".") else "unknown"

        # Check if the file already exists
        if UploadedFile.objects.filter(name=name, user=user).exists():
            messages.error(request, "A file with this name already exists.")
            return redirect("upload")

        # Create the UploadedFile object
        uploaded_file = UploadedFile.objects.create(
            user=user,
            name=name,
            type=file_type,
            file=file,
            description=description
        )

        # Handle thumbnail if provided
        if thumbnail:
            uploaded_file.thumbnail = thumbnail
            uploaded_file.save()

        messages.success(request, "File uploaded successfully")
        return redirect("upload")
    
    return render(request, 'upload.html', {"csrf_token": get_token(request)})

# File detail view with download tracking
@login_required
def uploaded_file_detail(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)

    # Check if the file exists before trying to download it
    if not file.file:
        messages.error(request, "This file is no longer available.")
        return redirect('files')  # Redirect to files list or wherever you want

    if request.method == "POST":
        # Check if the download button was clicked
        if "download" in request.POST:
            # Check if the user has already downloaded this file
            if not DownloadHistory.objects.filter(user=request.user, file=file).exists():
                # Record the download in DownloadHistory
                DownloadHistory.objects.create(user=request.user, file=file)

                # Increase the seed count
                file.seed_count += 1
                file.save()

                # Proceed with the actual file download
                response = redirect(file.file.url)
                response['Content-Disposition'] = f'attachment; filename={file.name}'
                return response
            else:
                messages.info(request, "You have already downloaded this file.")

    return render(request, 'uploaded_file_detail.html', {"file": file})

# Files listing view
def files(request):
    query = request.GET.get('search')  # Get the search query from the URL
    if query:  # If a search query is provided
        files = UploadedFile.objects.filter(name__icontains=query)  # Filter files by name
    else:  # If no search query is provided, render all files
        files = UploadedFile.objects.all()
    return render(request, 'files.html', {"query": query, "files": files})

# Delete file view
@login_required
def delete_file(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)

    # Ensure only the uploader can delete the file
    if file.user != request.user:
        messages.error(request, "You are not authorized to delete this file.")
        return redirect("uploaded_file_detail", pk=pk)

    # Delete the file
    file.delete()
    messages.success(request, "File deleted successfully.")
    return redirect("files")

# Profile view
@login_required
def profile_view(request, id):
    profile = get_object_or_404(StudentProfile, user__id=id)  # Fetch the profile by user ID
    uploaded_files = UploadedFile.objects.filter(user=profile.user).order_by('-uploaded_at')  # Fetch files uploaded by the user
    file_count = uploaded_files.count()

    if request.method == "POST" and request.FILES.get("profile_picture"):
        profile.profile_picture = request.FILES.get("profile_picture")
        profile.save()
        messages.success(request, "Profile picture updated successfully!")

    return render(request, 'profile.html', {"profile": profile, "uploaded_files": uploaded_files, "file_count": file_count})

# Settings view
@login_required
def settings_view(request):
    if request.method == "POST":
        # Get the updated data from the form
        username = request.POST.get("username")
        email = request.POST.get("email")
        std_id = request.POST.get("std_id")
        profile_picture = request.POST.get("profile_picture")

        # Update the user model
        user = request.user
        user.username = username
        user.email = email
        user.save()

        # Update the student profile model
        profile = StudentProfile.objects.get(user=user)
        profile.std_id = std_id
        profile.profile_picture = profile_picture  # Update the profile picture URL
        profile.save()

        messages.success(request, "Your information has been updated successfully!")
        return redirect("settings")

    # Render the settings page with the current user and profile data
    profile = StudentProfile.objects.get(user=request.user)
    return render(request, "settings.html", {"user": request.user, "profile": profile})
# Download History View
@login_required
def download_history(request):
    # Fetch download history for the logged-in user, ordered by the download date
    history = DownloadHistory.objects.filter(user=request.user).order_by('-downloaded_at')

    return render(request, 'download_history.html', {'history': history})
# Get chat messages
@login_required
def get_messages(request):
    messages = ChatMessage.objects.order_by('timestamp').values('user__username', 'message', 'timestamp')
    return JsonResponse(list(messages), safe=False)

# Save chat message
@csrf_exempt
@login_required
def save_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            if message:
                ChatMessage.objects.create(user=request.user, message=message)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Message is empty'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def user_uploads(request, username):
    # Get the user object based on the username
    user = get_object_or_404(User, username=username)
    
    # Fetch all files uploaded by this user
    user_files = UploadedFile.objects.filter(user=user).order_by('-uploaded_at')
    
    return render(request, 'user_uploads.html', {'user': user, 'user_files': user_files})