from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
	'''
	Renders a basic login homepage.
	'''
	# Get the request's context
	context = RequestContext(request)
	user = request.user

	# If user is logged in, redirect to home
	if user.is_active:
		return redirect('/student', user=user)

	return render_to_response(
		"home.html", 
		{}, 
		context)