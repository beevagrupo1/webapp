from Druzi.models import Activity, Enrollment
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ActivityForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def main(request):
    return render(request, 'webapp/main.html')

@login_required
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

def activity_pagination(request,page="1"):
    activity_list = Activity.objects.all()
    paginator = Paginator(activity_list, 10)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html', {"activity_list": list})

def activity_ultimos_propuestos_pagination(request,page="1"):
    activity_list = Activity.objects.all()
    paginator = Paginator(activity_list, 10)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html', {"activity_list": list})

def activity_mas_buscados_pagination(request,page="1"):
    activity_list = Activity.objects.all()
    paginator = Paginator(activity_list, 10)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html', {"activity_list": list})

def activity_mas_baratos_pagination(request,page="1"):
    activity_list = Activity.objects.all()
    paginator = Paginator(activity_list, 10)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html', {"activity_list": list})

def activity_mas_propuestos_pagination(request,page="1"):
    activity_list = Activity.objects.all()
    paginator = Paginator(activity_list, 10)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html', {"activity_list": list})

@login_required
def activity_enrrolment(request,id):
    activity = Activity.objects.get(id = id)
    enrollment = Enrollment(activity = activity,user = request.user)
    enrollment.save()
    messages.success(request,"Te has apuntado correctamente a la actividad")
    return HttpResponseRedirect(reverse('activity_list'))

@login_required
def activity_unenrrolment(request,id):
    activity = Activity.objects.get(id = id)
    enrollment = Enrollment.objects.get(activity = activity,user = request.user)
    enrollment.delete()
    messages.success(request,"Te has borrado correctamente a la actividad")
    return HttpResponseRedirect(reverse('activity_list'))