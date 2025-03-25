from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.middleware.csrf import get_token
from .models import StudentProfile, UploadedFile
from django.shortcuts import get_object_or_404
import os

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        Profile = StudentProfile.objects.get(user=request.user)
        latest_files = UploadedFile.objects.order_by('-uploaded_at')[:10]
        return render(request, 'home2.html', {"profile": Profile, "latest_files": latest_files})
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
        
        user = User.objects.create_user(username=name, email=email, password= password)
        StudentProfile.objects.create(user=user, std_id=std_id)

        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")
    
    return render(request, "register.html", {"csrf_token": get_token(request)})
def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        cuser = User.objects.get(email=email)
        user = authenticate(request, username=cuser.username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html', {"csrf_token": get_token(request)})
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')
def upload(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        file = request.FILES.get("file")
        type = file.content_type
        user = request.user

        # Check if the file already exists
        if UploadedFile.objects.filter(name=name, user=user).exists():
            messages.error(request, "A file with this name already exists.")
            return redirect("upload")

        # Get the file type from the file name
        file_extension = os.path.splitext(file.name)[1].lower()  # Extract the file extension
        if file_extension.startswith("."):
            file_type = file_extension[1:]  # Remove the leading dot (e.g., ".jpg" -> "jpg")
        else:
            file_type = "unknown"

        # Create the UploadedFile object
        UploadedFile.objects.create(
            user=user,
            name=name,
            type=file_type,
            file=file,
            description=description
        )
        messages.success(request, "File uploaded successfully")
        return redirect("upload")
    return render(request, 'upload.html', {"csrf_token": get_token(request)})
def uploaded_file_detail(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to view file details.")
        return redirect("login")

    file = get_object_or_404(UploadedFile, pk=pk)  # Fetch the file by its primary key
    return render(request, 'uploaded_file_detail.html', {"file": file})