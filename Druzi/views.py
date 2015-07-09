from django.db.models import Q
from django.db.models import Count
import operator
import re
from datetime import datetime
from Druzi.models import Activity, Enrollment, Tag, TagAppear
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
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
            tags = re.compile("\S*#(?:\[[^\]]+\]|\S+)").findall(activity.description)
            for t in tags:
                pos =  activity.description.index(t)
                temp = Tag.objects.get_or_create(name = t[1:])[0]
                temp.count = temp.count+1
                temp.save()
                if temp:
                    TagAppear(activity = activity, tag = temp, position = pos).save()
                else:
                    tag = Tag(name = t[1:]).save()
                    TagAppear(activity = activity, tag = tag, position = pos).save()
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
    activity_list = Activity.objects.filter(activity_date__gte = datetime.now()).order_by('-creation_date')
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
    activity_list = Activity.objects.all().order_by("-visit_count")
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
    activity_list = Activity.objects.filter(activity_date__gte = datetime.now()).order_by('price')
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
    activity_list = Activity.objects.raw('SELECT *, COUNT(*) AS "repeat" FROM Druzi_activity WHERE Druzi_activity.parent_id IS NOT NULL GROUP BY Druzi_activity.parent_id ORDER BY 13 DESC')
    paginator = Paginator(activity_list, 10)
    paginator._count = len(list(activity_list))
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html', {"activity_list": lista})

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

def tags_autocomplete(request, text):
    text = text.replace('+','')
    tags = Tag.objects.filter(name__startswith = text)
    for tag in tags:
        tag.name = '#' + tag.name
    data = serializers.serialize('json', tags)
    return HttpResponse(data, content_type='application/json')

def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        query = request.POST
        first = True
        list = None
        for i, criteria in enumerate(query["query"].split(',')):
            if criteria[0]=='#':
                if (first):
                    list = Activity.objects.filter(tags__name=criteria.replace('#',''))
                    first = False
                else:
                    list = list.filter(tags__name=criteria.replace('#',''))
            else:
                if (first):
                    list = Activity.objects.filter(description__search=criteria)
                    first = False
                else:
                    list = list.filter(description__search=criteria)
        return render(request, 'webapp/activity_list.html', {"activity_list": list})
    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponseRedirect('/')

def activity_details(request,id):
    activity = Activity.objects.get(id=id)
    activity.visit_count = activity.visit_count+1
    activity.save()
    return render(request, 'webapp/activity_details.html', {"activity": activity})
