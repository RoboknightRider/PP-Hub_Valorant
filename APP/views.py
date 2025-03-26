from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.middleware.csrf import get_token
from .models import StudentProfile, UploadedFile
from django.shortcuts import get_object_or_404
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
from django.contrib.auth.decorators import login_required
import json

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
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
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
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to upload file.")
        return redirect("login")
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
def files(request):
    query = request.GET.get('search')  # Get the search query from the URL
    try:
        if query:  # If a search query is provided
            print(f"Searching for files with query: {query}")  # Debugging log
            files = UploadedFile.objects.filter(name__icontains=query)  # Filter files by name
        else:  # If no search query is provided, render all files
            print("No search query provided. Fetching all files.")  # Debugging log
            files = UploadedFile.objects.all()

        # Optional: Add pagination
        from django.core.paginator import Paginator
        paginator = Paginator(files, 10)  # Show 10 files per page
        page_number = request.GET.get('page')
        files_page = paginator.get_page(page_number)

        return render(request, 'files.html', {"query": query, "files": files_page})
    except Exception as e:
        print(f"Error fetching files: {str(e)}")  # Debugging log
        messages.error(request, "An error occurred while fetching files.")
        return redirect('home')

@login_required
def get_messages(request):
    messages = ChatMessage.objects.order_by('timestamp').values('user__username', 'message', 'timestamp')
    return JsonResponse(list(messages), safe=False)

@csrf_exempt
@login_required
def save_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            if message:
                print(f"Saving message: {message} from user: {request.user.username}")  # Debugging log
                ChatMessage.objects.create(user=request.user, message=message)
                return JsonResponse({'status': 'success'})
            else:
                print("Error: Message is empty")  # Debugging log
                return JsonResponse({'status': 'error', 'message': 'Message is empty'}, status=400)
        except json.JSONDecodeError:
            print("Error: Invalid JSON")  # Debugging log
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Error: {str(e)}")  # Debugging log
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    print("Error: Invalid request method")  # Debugging log
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)