from django.conf.urls import patterns, url
from student import views

urlpatterns = patterns('',
    url(r'^$', views.student_home, name='student_home'),
    )