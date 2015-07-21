from django.db.models import Q
from django.db.models import Count
import operator
import re
from datetime import datetime
from Druzi.models import Activity, Enrollment, Tag, TagAppear, Rating
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import ActivityForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils import timezone


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
            description = activity.description
            for t in tags:
                pos = activity.description.index(t)
                temp = Tag.objects.get_or_create(name=t[1:])[0]
                description = description.replace(t, '<a href="/search/tag/' + temp.name + '/">' + t + '</a>')
                temp.count = temp.count + 1
                temp.save()
                if temp:
                    TagAppear(activity=activity, tag=temp, position=pos).save()
                else:
                    tag = Tag(name=t[1:]).save()
                    TagAppear(activity=activity, tag=tag, position=pos).save()
            activity.description = description
            activity.save()
            messages.success(request, 'Se ha creado correctamente la actividad')
            return HttpResponseRedirect(reverse('activity_details', kwargs={'slug' : activity.get_slug , 'id': activity.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ActivityForm()

    return render(request, 'webapp/actvity_creation.html', {'form': form})


def activity_pagination(request, page="1"):
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

    return render(request, 'webapp/activity_list.html',
                  {"activity_list": list, 'url': 'activity_list_page'})


def activity_ultimos_propuestos_pagination(request, page="1"):
    activity_list = Activity.objects.filter(activity_date__gte=datetime.now()).order_by('-creation_date')
    paginator = Paginator(activity_list, 10)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html',
                  {"activity_list": list, 'url': 'activity_ultimos_propuestos_pagination'})


def activity_mas_buscados_pagination(request, page="1"):
    activity_list = Activity.objects.filter(activity_date__gte=datetime.now()).order_by("-visit_count")
    paginator = Paginator(activity_list, 10)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html',
                  {"activity_list": list, 'url': 'activity_mas_buscados_pagination'})


def activity_mas_baratos_pagination(request, page="1"):
    activity_list = Activity.objects.filter(activity_date__gte=datetime.now()).order_by('price')
    paginator = Paginator(activity_list, 10)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html',
                  {"activity_list": list, 'url': 'activity_mas_baratos_pagination'})


def activity_mas_propuestos_pagination(request, page="1"):
    activity_list = Activity.objects.raw(
        'SELECT *, COUNT(*) AS "repeat" FROM Druzi_activity WHERE Druzi_activity.parent_id IS NOT NULL GROUP BY Druzi_activity.parent_id ORDER BY 13 DESC')
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

    return render(request, 'webapp/activity_list.html',
                  {"activity_list": lista, 'url': 'activity_mas_propuestos_pagination'})


@login_required
def activity_mylist_pagination(request, page="1"):
    activity_list = Activity.objects.filter(participants=request.user).order_by('-activity_date')
    paginator = Paginator(activity_list, 10)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html',
                  {"activity_list": lista, 'url': 'activity_mylist_pagination'})


@login_required
def activity_enrrolment(request, slug, id):
    activity = Activity.objects.get(id=id)
    enrollment = Enrollment(activity=activity, user=request.user)
    count_participants = activity.participants.all().count()
    if activity.activity_date <= timezone.now() :
        messages.warning(request, "No te puedes inscribir, la actividad ya esta cerrada")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else :
        if count_participants >= activity.limit_participants and activity.limit_participants!=0:
            messages.warning(request, "No te puedes inscribir, se ha superado el limite de participantes")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else :
            enrollment.save()
            messages.success(request, "Te has apuntado correctamente a la actividad")
            return HttpResponseRedirect(reverse('activity_details', kwargs={'slug' : activity.get_slug, 'id': id}))

@login_required
def activity_unenrrolment(request, slug, id):
    activity = Activity.objects.get(id=id)
    enrollment = Enrollment.objects.get(activity=activity, user=request.user)
    if activity.activity_date <= timezone.now() :
        messages.warning(request, "No te puedes borrar, la actividad ya esta cerrada")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else :
        enrollment.delete()
        messages.success(request, "Te has borrado correctamente a la actividad")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def activity_repeat(request, slug, id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ActivityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user_own = request.user
            activity.parent_id = id
            activity.save()
            tags = re.compile("\S*#(?:\[[^\]]+\]|\S+)").findall(activity.description)
            description = activity.description
            for t in tags:
                pos = activity.description.index(t)
                temp = Tag.objects.get_or_create(name=t[1:])[0]
                description = description.replace(t, '<a href="/search/tag/' + temp.name + '/">' + t + '</a>')
                temp.count = temp.count + 1
                temp.save()
                if temp:
                    TagAppear(activity=activity, tag=temp, position=pos).save()
                else:
                    tag = Tag(name=t[1:]).save()
                    TagAppear(activity=activity, tag=tag, position=pos).save()
            activity.description = description
            activity.save()
            messages.success(request, 'Se ha creado correctamente la actividad')
            return HttpResponseRedirect(reverse('activity_details', kwargs={'slug' : activity.get_slug, 'id': activity.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        activity = Activity.objects.get(id=id)
        new_activity = activity.clone(request.user)
        form =  ActivityForm(instance=new_activity)

    return render(request, 'webapp/actvity_creation.html', {'form': form})


def tags_autocomplete(request, text):
    text = text.replace('+', '')
    tags = Tag.objects.filter(name__startswith=text)
    for tag in tags:
        tag.name = '#' + tag.name
    data = serializers.serialize('json', tags)
    return HttpResponse(data, content_type='application/json')


def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        query = request.POST
        first = True
        list = []
        if query["query"] == "":
            messages.info(request, "Tienes que introducir algun valor de busqueda, si ya lo has introducido, recuerda pulsar al ENTER antes de dar al boton Buscar")
            return HttpResponseRedirect('/')
        else:
            for i, criteria in enumerate(query["query"].split(',')):
                if criteria[0] == '#':
                    if (first):
                        list = Activity.objects.filter(tags__name=criteria.replace('#', ''))
                        first = False
                    else:
                        list = list.filter(tags__name=criteria.replace('#', ''))
                else:
                    if (first):
                        list = Activity.objects.filter(description__search=criteria)
                        first = False
                    else:
                        list = list.filter(description__search=criteria)
            return render(request, 'webapp/activity_list.html', {"activity_list": list})
    else:
        return HttpResponseRedirect('/')


def search_tag(request, tag):
    list = Activity.objects.filter(tags__name=tag)
    return render(request, 'webapp/activity_list.html', {"activity_list": list})


def activity_details(request, slug, id):
    activity = Activity.objects.get(id=id)
    activity.visit_count = activity.visit_count + 1
    activity.save()
    user_rating = activity.rating_set.filter(user = request.user)
    if user_rating.count()>0:
        user_rating = user_rating[0]
    else:
        user_rating = None
    return render(request, 'webapp/activity_details.html', {"activity": activity, "user_rating" : user_rating})

def stars_post(request, id):
    activity = Activity.objects.get(id=id)
    rating = Rating.objects.filter(activity=activity, user=request.user)
    if rating.count() == 0:
        if request.method == 'POST':
            rating_val = request.POST['rating']
            rating_val = float(rating_val)
            rating_obj = Rating(activity=activity, user = request.user, rating=rating_val)
            activity.sum_rating = activity.sum_rating + rating_val
            activity.count_rating = activity.count_rating + 1
            activity.save()
            rating_obj.save()
        return HttpResponse("ok", content_type='application/text')
    else:
        return HttpResponse("Ya habias votado esta actividad", content_type='application/text')

@login_required
def activity_list_repeat(request, slug, id, page="1"):
    activity_list = Activity.objects.filter(Q(parent_id=id) | Q(id=id))
    paginator = Paginator(activity_list, 10)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista = paginator.page(paginator.num_pages)

    return render(request, 'webapp/activity_list.html',
                  {"activity_list": lista, 'url': 'activity_list_repeat', 'origin' : int(id)})
                   
@login_required
def activity_remove(request, slug, id):
    activity = Activity.objects.get(id=id)
    if request.user == activity.user_own:
        if activity.is_enable:
            activity.delete()
            messages.success(request, "Has borrado correctamente a la actividad")
        else:
            messages.warning(request, "Estas intentando borrar una actividad en un tiempo excesivo")
    else:
        messages.warning(request, "Estas intentando borrar una actividad que no has creado tu")
    return HttpResponseRedirect('/')

@login_required
def activity_modify(request, slug, id):
    activity = Activity.objects.get(id=id)
    if request.user == activity.user_own:
        if activity.is_enable:
            # if this is a POST request we need to process the form data
            if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = ActivityForm(request.POST)
                # check whether it's valid:
                if form.is_valid():
                    activity_form = form.save(commit=False)
                    
                    activity.title = activity_form.title
                    activity.description = activity_form.description
                    activity.activity_date = activity_form.activity_date
                    activity.position = activity_form.position
                    activity.place_name = activity_form.place_name
                    activity.price = activity_form.price
                    activity.limit_participants = activity_form.limit_participants
                    activity.tags.clear()
                    
                    tags = re.compile("\S*#(?:\[[^\]]+\]|\S+)").findall(activity.description)
                    description = activity.description
                    for t in tags:
                        pos = activity.description.index(t)
                        temp = Tag.objects.get_or_create(name=t[1:])[0]
                        description = description.replace(t, '<a href="/search/tag/' + temp.name + '/">' + t + '</a>')
                        temp.count = temp.count + 1
                        temp.save()
                        if temp:
                            TagAppear(activity=activity, tag=temp, position=pos).save()
                        else:
                            tag = Tag(name=t[1:]).save()
                            TagAppear(activity=activity, tag=tag, position=pos).save()
                    activity.description = description
                    activity.save()
                    messages.success(request, 'Se ha modificado correctamente la actividad')
                    return HttpResponseRedirect(reverse('activity_details', kwargs={'slug' : slug , 'id': activity.id}))
        
            # if a GET (or any other method) we'll create a blank form
            else:
                activity = Activity.objects.get(id=id)
                activity.description = activity.get_description_text
                form = ActivityForm(instance=activity)
            return render(request, 'webapp/actvity_creation.html', {'form': form})
        else:
            messages.warning(request, "Estas intentando modificar una actividad en un tiempo excesivo")
    else:
        messages.warning(request, "Estas intentando modificar una actividad que no has creado tu")
    return HttpResponseRedirect('/')

        
def about_us(request):

    return render(request, 'webapp/about_us.html')      



def offer(request):
    return render(request, 'webapp/offer.html')
