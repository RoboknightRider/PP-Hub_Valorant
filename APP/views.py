from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .models import StudentProfile, UploadedFile, ChatMessage
from .utils import generate_torrent_and_magnet

def home(request):
    """
    If the user is not authenticated, render a public homepage.
    Otherwise, display a protected homepage with the user's profile and 
    the 10 most recent uploaded files.
    """
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        profile = StudentProfile.objects.get(user=request.user)
        latest_files = UploadedFile.objects.order_by('-uploaded_at')[:10]
        return render(request, 'home2.html', {"profile": profile, "latest_files": latest_files})

def login_view(request):
    """
    Handle user login. On POST, authenticate the user and log them in.
    On GET, render the login page.
    """
    if request.method == 'POST':
        # Retrieve username and password from POST data.
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user.
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    
    return render(request, 'login.html', {"csrf_token": get_token(request)})

def logout_view(request):
    """
    Log out the current user and redirect to the homepage.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def register(request):
    """
    Handle user registration. Validate form data and create a new user and 
    associated StudentProfile if all validations pass.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        std_id = request.POST.get('std_id')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([username, std_id, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "A user with this username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        # Create a corresponding StudentProfile entry.
        StudentProfile.objects.create(user=user, std_id=std_id)

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'register.html', {"csrf_token": get_token(request)})

def upload(request):
    """
    Handle file uploads. This view validates the input, determines the file type 
    (either from the form's dropdown or from the file extension) and then creates 
    an UploadedFile instance. After creation, it attempts to generate torrent 
    information.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to upload a file.")
        return redirect("login")
    
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        file_type_from_form = request.POST.get("file_type")
        file = request.FILES.get("file")
        
        if not file:
            messages.error(request, "No file provided.")
            return redirect("upload")
        
        # Determine file extension as a fallback.
        file_extension = os.path.splitext(file.name)[1].lower()
        computed_file_type = file_extension[1:] if file_extension.startswith(".") else "unknown"
        file_type = file_type_from_form if file_type_from_form else computed_file_type
        
        user = request.user
        if UploadedFile.objects.filter(name=name, user=user).exists():
            messages.error(request, "A file with this name already exists.")
            return redirect("upload")
        
        uploaded_obj = UploadedFile.objects.create(
            user=user,
            name=name,
            type=file_type,
            file=file,
            description=description
        )
        
        try:
            generate_torrent_and_magnet(uploaded_obj)
        except Exception as e:
            messages.warning(request, f"File uploaded but torrent generation failed: {e}")
            return redirect("upload")
        
        messages.success(request, "File uploaded successfully. Torrent information is now available.")
        return redirect("upload")
    
    return render(request, 'upload.html', {"csrf_token": get_token(request)})

def uploaded_file_detail(request, pk):
    """
    Display detailed information about a specific uploaded file.
    The view fetches the file object and renders the detail template.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to view file details.")
        return redirect("login")
    
    file_object = get_object_or_404(UploadedFile, pk=pk)
    return render(request, 'uploaded_file_detail.html', {"file": file_object})

def files(request):
    """
    Display a list of uploaded files.
    If a search query is provided via GET parameter 'search', filter the files by name.
    """
    query = request.GET.get('search')
    if query:
        files_list = UploadedFile.objects.filter(name__icontains=query)
    else:
        files_list = UploadedFile.objects.all()
    
    return render(request, 'files.html', {"query": query, "files": files_list})

def delete_file(request, pk):
    """
    Delete an uploaded file if the current user is the owner.
    The view checks authorization, then deletes the file, and shows appropriate messages.
    """
    file_obj = get_object_or_404(UploadedFile, pk=pk)
    
    # Ensure that only the uploader can delete the file.
    if file_obj.user != request.user:
        messages.error(request, "You are not authorized to delete this file.")
        return redirect("uploaded_file_detail", pk=pk)
    
    file_obj.delete()
    messages.success(request, "File deleted successfully.")
    return redirect("files")

def profile_view(request):
    """
    Display the logged-in user's profile page along with a list of files uploaded by them.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to view your profile.")
        return redirect("login")
    
    profile = StudentProfile.objects.get(user=request.user)
    uploaded_files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')
    file_count = uploaded_files.count()
    
    context = {
        "profile": profile,
        "uploaded_files": uploaded_files,
        "file_count": file_count,
    }
    return render(request, 'profile.html', context)

def settings_view(request):
    """
    Display and handle updates to the user's settings.
    
    For GET requests:
      - Retrieves the current user's profile and displays their settings in the form.
    
    For POST requests:
      - Retrieves updated settings (username, email, and student ID) from the form,
        updates the corresponding User and StudentProfile objects, and then
        displays a success message.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view settings.")
        return redirect("login")
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        std_id = request.POST.get("std_id")
        
        user = request.user
        user.username = username
        user.email = email
        user.save()
        
        profile = StudentProfile.objects.get(user=user)
        profile.std_id = std_id
        profile.save()
        
        messages.success(request, "Your information has been updated successfully!")
        return redirect("settings")
    else:
        profile = StudentProfile.objects.get(user=request.user)
        return render(request, "settings.html", {"user": request.user, "profile": profile})

def get_messages(request):
    """
    Retrieve chat messages in JSON format.
    Messages are ordered by their timestamp.
    """
    messages_qs = ChatMessage.objects.order_by('timestamp').values('user__username', 'message', 'timestamp')
    return JsonResponse(list(messages_qs), safe=False)

@csrf_exempt
@login_required
def save_message(request):
    """
    Save a chat message sent via an AJAX call.
    Expects a POST request with JSON data containing a 'message' field.
    Returns a JSON response indicating success or error.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message_text = data.get('message', '').strip()
            if message_text:
                ChatMessage.objects.create(user=request.user, message=message_text)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Message is empty'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
