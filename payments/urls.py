from django.conf.urls import patterns, url
from payments import views

urlpatterns = patterns('',
	url(r'^process_new_card', views.process_new_card, name='process_new_card'),
    )
