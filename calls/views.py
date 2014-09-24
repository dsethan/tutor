from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from twilio.rest import TwilioRestClient
from users.models import UserProfile, TutorProfile
from django.contrib.auth.models import User
from schools.models import School
from classes.models import Class
from departments.models import Department
from session.models import Session
from tutorclass.models import TutorClass
from calls.models import Call
import re

# Create your views here.

def call_process(request):
	# Get this request's context
	context = RequestContext(request)

	# Get objects called through the HTTP POST request
	if request.method == 'POST':

		# Get class id from the POST and associated Class object
		class_id = request.POST.get('class')
		requested_class = Class.objects.get(id=int(class_id))

		# Construct a new Call object
		call_to_add = Call(teach=requested_class)

		call_to_add.save()

		return HttpResponse("Your tutor is being requested. You will get a text when you get a match.")

	return HttpResponse("Got here.")