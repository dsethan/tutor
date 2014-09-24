from django.conf.urls import patterns, url
from calls import views

urlpatterns = patterns('',
    url(r'^$', views.call_process, name='call_process'),

    )