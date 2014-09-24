from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
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

@login_required
def tutor_home(request):
	# Get the request's context
	context = RequestContext(request)

	# Get user
	user = request.user

	if is_tutor(user):

		# Get associated TutorProfile
		tutor = get_tutor_profile(user)

		classes = []

		# Get all classes I teach
		for c in TutorClass.objects.all():
			if c.tutor == tutor:
				classes.append(c.teach)

		active_calls = []
		# Check to see if any of these have an active Call
		for call in Call.objects.all():
			if (call.teach in classes) and call.is_active():
				active_calls.append(call)

		return render_to_response(
			"tutor_home.html",
			{'tutor':tutor,
			'active_calls':active_calls},
			context)

	return HttpResponse("Denied")


def is_tutor(user):
	# Check to see if a TutorProfile object is associated
	# with this User

	for tp in TutorProfile.objects.all():
		if tp.user == user:
			return True

	return False

def get_tutor_profile(user):
	# Get associated TutorProfile
	# with this User

	for tp in TutorProfile.objects.all():
		if tp.user == user:
			return tp

	return False