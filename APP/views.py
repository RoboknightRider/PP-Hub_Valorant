from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.middleware.csrf import get_token
from .models import StudentProfile, UploadedFile

def home(request):
    return render(request, 'home.html')
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
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html', {"csrf_token": get_token(request)})
def dashboard(request):
    if not request.user.is_authenticated:
       return redirect('home') 
    
    Profile = StudentProfile.objects.get(user=request.user)
    return render(request, 'dashboard.html', {"profile": Profile})
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
        UploadedFile.objects.create(user=user, name=name, type=type, file=file, description=description)
        messages.success(request, "File uploaded successfully")
        return redirect("dashboard")
    return render(request, 'upload.html', {"csrf_token": get_token(request)})