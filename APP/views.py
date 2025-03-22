from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .mongodb import users_collection
from django.contrib.auth.hashers import make_password

def home(request):
    return render(request, 'home.html')
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        user_id = request.POST.get("id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        # Validation: Check if any field is empty
        if not all([name, user_id, email, password, confirm_password]):
            messages.error(request, "All fields are required")
            return redirect("register")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Password do not match")
            return redirect("register")

        # Check if user already exists (by ID or email)
        if users_collection.find_one({"$or": [{"id": user_id}, {"email": email}]}):
            messages.error(request, "User ID or Email already exists")
            return redirect("register")

        # Insert new user into MongoDB (with hashed password)
        hashed_password = make_password(password)
        users_collection.insert_one({
            "name": name,
            "id": user_id,
            "email": email,
            "password": hashed_password
        })

        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")
    
    return render(request, "register.html")
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home') 
    return render(request, 'dashboard.html')
def logout(request):
    return render(request, 'logout.html')