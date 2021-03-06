"""projectdruzi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^login/$', auth_views.login, {'template_name': 'webapp/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page':'main'}, name='logout'),
    url(r'^profile/(?P<username>[.\w]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[.\w]+)/page/(?P<page>[0-9]+)/$', views.profile, name='profile_page'),
    url(r'^activity/creation/$', views.activity_creation, name='activity_creation'),
    url(r'^activity/list/$', views.activity_pagination, name='activity_list'),
    url(r'^activity/list/page/(?P<page>[0-9]+)/$', views.activity_pagination, name='activity_list_page'),
    url(r'^activity/(?P<slug>[-\w\d]+),(?P<id>\d+)/repeat/list/$', views.activity_list_repeat, name='activity_list_repeat'),
    url(r'^activity/(?P<slug>[-\w\d]+),(?P<id>\d+)/repeat/list/page/(?P<page>[0-9]+)/$', views.activity_list_repeat, name='activity_list_repeat_page'),
    url(r'^activity/baratas/list/$', views.activity_mas_baratos_pagination, name='activity_mas_baratos_pagination'),
    url(r'^activity/baratas/list/page/(?P<page>[0-9]+)/$', views.activity_mas_baratos_pagination, name='activity_mas_baratos_pagination'),
    url(r'^activity/buscados/list/$', views.activity_mas_buscados_pagination, name='activity_mas_buscados_pagination'),
    url(r'^activity/buscados/list/page/(?P<page>[0-9]+)/$', views.activity_mas_buscados_pagination, name='activity_mas_buscados_pagination'),
    url(r'^activity/ultimos/list/$', views.activity_ultimos_propuestos_pagination, name='activity_ultimos_propuestos_pagination'),
    url(r'^activity/ultimos/list/page/(?P<page>[0-9]+)/$', views.activity_ultimos_propuestos_pagination, name='activity_ultimos_propuestos_pagination'),
    url(r'^activity/propuestos/list/$', views.activity_mas_propuestos_pagination, name='activity_mas_propuestos_pagination'),
    url(r'^activity/propuestos/list/page/(?P<page>[0-9]+)/$', views.activity_mas_propuestos_pagination, name='activity_mas_propuestos_pagination'),
    url(r'^activity/(?P<slug>[-\w\d]+),(?P<id>\d+)/$', views.activity_details, name='activity_details'),
    url(r'^activity/(?P<slug>[-\w\d]+),(?P<id>\d+)/repeat$', views.activity_repeat, name='activity_repeat'),
    url(r'^activity/(?P<slug>[-\w\d]+),(?P<id>\d+)/enrollment$', views.activity_enrrolment, name='activity_enrrollment'),
    url(r'^activity/(?P<slug>[-\w\d]+),(?P<id>\d+)/unenrollment$', views.activity_unenrrolment, name='activity_unenrrollment'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/tag/(?P<tag>.*)/$', views.search_tag, name='search_tag'),
    url(ur'^tags/(?P<text>.*)/$', views.tags_autocomplete, name='tags_autocomplete'),
    url(r'^activity/mylist/list/$', views.activity_mylist_pagination, name='my_list'),
    url(r'^activity/mylist/list/page/(?P<page>[0-9]+)/$', views.activity_mylist_pagination, name='my_list_page'),
    url(r'^activity/(?P<slug>[-\w\d]+),(?P<id>[.\w]+)/remove$', views.activity_remove, name='activity_remove'),
    url(r'^activity/(?P<slug>[-\w\d]+),(?P<id>[.\w]+)/modify$', views.activity_modify, name='activity_modify'),
    url(r'^activity/get/(?P<id>[.\w]+)/stars_post/$', views.stars_post, name='stars_post'),
    url(r'^email-sent/', views.validation_sent, name='email_sent'),
    url(r'^email/$', views.require_email, name='require_email'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^about_us/#(?P<anchor>.*)$', views.about_us, name='about_us_a'),

]
