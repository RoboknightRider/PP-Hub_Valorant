from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    return render(request, 'Nigga.html')
def home(request):
    return render(request, 'homepage.html')