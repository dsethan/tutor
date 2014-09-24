from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('web.urls')),
    url(r'^u/', include('users.urls')),
	url(r'^payments/', include('payments.urls')),
	url(r'^dashboard/', include('dashboard.urls')),
	url(r'^student/', include('student.urls')),
	url(r'^calls/', include('calls.urls')),
	url(r'^tutors/', include('tutors.urls')),


    url(r'^sms/$', 'views.sms'),
    url(r'^ring/$', 'views.ring'),

)
