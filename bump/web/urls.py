from django.conf.urls import patterns, url
from web import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    )