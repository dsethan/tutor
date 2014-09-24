from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
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
import re

@login_required
def student_home(request):
	# Get the request's context
	context = RequestContext(request)

	# Get current user's info
	user = request.user

	# Make sure that the current user is logged in
	if user.is_active:

		# Get associated UserProfile
		profile = get_user_profile(user)

		# Get associated school and phone number
		school = profile.school
		phone = profile.phone

		# Create a list of all classes offered at 
		# the user's school
		classes = []

		for c in Class.objects.all():
			if c.department.school == school:
				classes.append(c)

		# Get all active classes at this particular school
		active_classes = []

		for tc in TutorClass.objects.all():
			if (tc.teach.department.school == school) and (tc.tutor.is_active):
				if tc.teach not in active_classes:
					active_classes.append(tc.teach)


		active_classes = set(active_classes)
		classes = set(classes)

		return render_to_response("student_home.html",
			{'classes':classes,
			'user':user,
			'profile':profile,
			'school':school,
			'active_classes':active_classes},
			context)

	# TODO: Fix this into a better error page
	return HttpResponse("Error.")







def get_user_profile(user):
	# Loop through all user objects to find user profile
	for u in UserProfile.objects.all():
		if u.user == user:
			return u

	# Otherwise, return False
	return False

