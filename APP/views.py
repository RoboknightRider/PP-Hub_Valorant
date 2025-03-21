from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')
def register(request):
    return render(request, 'register.html')
def login(request):
    return render(request, 'login.html')
def dashboard(request):
    return render(request, 'dashboard.html')
def logout(request):
    return render(request, 'logout.html')