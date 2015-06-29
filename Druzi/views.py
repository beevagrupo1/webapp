import django
from django.shortcuts import render
import views

# Create your views here.

def main(request):
    return render(request, 'webapp/main.html')