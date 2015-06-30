import django
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
import views
from .forms import ActivityForm
from .models import Activity

# Create your views here.

def main(request):
    return render(request, 'webapp/main.html')

def activity_creation(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ActivityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user_own = request.user
            activity.save()
            messages.success(request, 'Se ha creado correctamente la actividad')
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ActivityForm()

    return render(request, 'webapp/actvity_creation.html', {'form': form})