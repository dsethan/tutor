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
import student.views
import re

def register(request):
	'''
	Renders an empty registration page for new UserProfiles (client side).
	'''
	# Get request's context
	context = RequestContext(request)

	# Get list of all schools to pass through to the view
	schools = School.objects.all()

	# Render the register form, pass through the list of schools
	return render_to_response(
		"register.html",
		{'schools': schools},
		context)


def process(request):
	'''
	Processes the form submitted in registration.
	'''
	# Get request's context
	context = RequestContext(request)

	if request.method == 'POST':
		# Initialize an error list to send back to the registration page if needed
		errors = []

		# Pull all of the post variables submitted in the form
		username = request.POST.get('username')
		first = request.POST.get('first')
		last = request.POST.get('last')
		phone = request.POST.get('phone')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		school = request.POST.get('school')
		print "School" + str(school)

		# Make sure passwords match
		match = passwords_match(password1, password2)

		# Make sure user object w/ submitted username does not already exist
		user_exists = False

		for u in User.objects.all():
			if u.username == username:
				user_exists = True

		# Make the phone, first, and last variables clean
		clean_user = clean_email(username)
		clean_first = clean(first)
		clean_last = clean(last)
		clean_num = clean_phone(phone)

		if (match == True) and (user_exists == False) and (clean_num != False) and (clean_first != False) and (clean_last != False) and (clean_email != False):
			# Construct the new object
			user_to_add = User(
				username=clean_user,
				first_name=clean_first,
				last_name=clean_last)

			# And the password
			user_to_add.set_password(password1)

			# Save the new user into the database
			user_to_add.save()

			# Now add the new user profile
			user_profile_to_add = UserProfile(
				user=user_to_add,
				phone=clean_num,
				school=School.objects.get(id=school))

			# Save the user profile
			user_profile_to_add.save()

			# Send user profile's ID to the add payment view
			user_to_add = user_to_add.id
			
			return render_to_response(
				'add_payment.html',
				{'user_to_add':user_to_add},
				context)

		else:

			# Get list of all schools to pass through to the view
			schools = School.objects.all()

			# Check to see what errors are being thrown
			if (match == False):
				errors.append("Your passwords do not match.")
			if (clean_user == False):
				errors.append("Please enter a valid email.")
			if (user_exists == True):
				errors.append("This user already exists.")
			if (clean_num == False):
				errors.append("Please enter a valid phone number.")
			if (clean_first == False) or (clean_last == False):
				errors.append("Please enter a first and last name.")

			# Return original register template, with errors listed
			return render_to_response("register.html",
				{'schools':schools,
				'errors':errors},
				context)

	return register(request)
def clean_email(username):
	'''
	Checks to make sure that username is valid (meaning it is in email form).
	'''
	if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", username):
		return False

	return username

def clean(name):
	'''
	Transforms a submitted name element into something cleaner.
	If name is somehow invalid, return "False"
	Examples:
	"ethan" --> "Ethan"
	"ethAn" --> "Ethan"
	"ETHAN" --> "Ethan"
	'''
	# Need length of name to be greater than 0
	if len(name) == 0:
		return False

	# Return the name in title format
	return name.title()

def clean_phone(num):
	'''
	Transforms a submitted phone element into something cleaner.
	If digits are invalid, returns "False"
	Examples:
	"9999999999" --> "+19999999999"
	"999-999-9999" --> "+19999999999"
	"99999999999" --> False
	'''
	# Initialize a cleaned string
	clean = ""
	# Loop through each submitted character
	for i in range(len(num)):
		if num[i].isdigit():
			clean = clean + num[i]

	# Checks to see if this is of valid length
	# CASE 1: Correct # of digits have been entered for area code + num
	if len(clean) == 10:
		return "+1" + clean

	# CASE 2: Correct # of digits have been entered, including country code
	if (len(clean) == 11) and (clean[0] == 1):
		return "+" + clean

	return False

def passwords_match(pw1, pw2):
	'''
	Checks to see if two passwords from registration form match.
	'''
	if (pw1 == pw2) and (len(pw1) > 0):
		return True
	return False


def user_login(request):
	'''
	Handles login requests
	'''
	# Get the request's context and find out which user is currently trying
	# to log in
	context = RequestContext(request)
	current_user = request.user

	# If current user is active, just bring them to their home page
	# TODO: Bring a tutor to a separate view.
	if current_user.is_active:
		return redirect(student.views.student_home)

	# In case of a HTTP POST request
	if request.method == 'POST':
		# Get the username and login combo that the user tried to log in with
		username = request.POST['username']
		password = request.POST['password']

		print username
		print password
		# Authenticate the username/password combination
		user = authenticate(username=username, password=password)

		print user

		# If our user object is returned, try to log in
		if user is not None:

			# Make sure account if active
			if user.is_active:

				# Now we can log this user in
				login(request, user)

				# And bring them to their homepage
				return redirect(student.views.student_home)

			# If account is not active, then return an error
			else:
				return HttpResponse("This account is disabled.")

		# Invalid login details supplied. Send this information over

		else:
			errors = ["You have provided an invalid username/password combination."]
			return render_to_response(
				"home.html",
				{'errors':errors},
				context)
	else:
		return render_to_response(
			"home.html",
			context)