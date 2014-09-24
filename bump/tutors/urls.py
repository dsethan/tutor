from django.conf.urls import patterns, url
from tutors import views

urlpatterns = patterns('',
    url(r'^$', views.tutor_home, name='tutor_home'),
    )