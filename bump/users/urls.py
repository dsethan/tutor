from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^register', views.register, name='register'),
	url(r'^process', views.process, name='process'),
    url(r'^user_login', views.user_login, name='user_login'),

    )
