from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^process', views.process, name='process'),
    url(r'^class_process', views.class_process, name='class_process'),

    )