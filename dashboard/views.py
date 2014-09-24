from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from schools.models import School
from users.models import UserProfile, TutorProfile
from django.contrib.auth.models import User
from departments.models import Department
from classes.models import Class
from tutorclass.models import TutorClass
import re

def dashboard(request):
	# Get the request's context
	context = RequestContext(request)

	# Get current user
	user = request.user

	# Pass through a list of numbers
	nums = [1,2,3,4,5,6,7,8]

	# Get list of all schools to pass through to the view
	schools = School.objects.all()

	# See if user has permission to enter site
	if user.is_superuser:
		return render_to_response(
			"dashboard.html",
			{'nums':nums,
			'schools':schools},
			context)

	# If not allowed, return basic HTTP page with a message
	return HttpResponse("Access denied")



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
		num = request.POST.get('number')
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

			# Now add the new tutor profile
			user_profile_to_add = TutorProfile(
				user=user_to_add,
				phone=clean_num,
				school=School.objects.get(id=school))

			# Save the user profile
			user_profile_to_add.save()

			# Send through user_to_add's id
			user_to_add_id = user_to_add.id

			# Send user profile's ID to the add payment view
			user_to_add = User.objects.get(id=user_to_add.id)
			
			# Send total num
			total = num

			# Send list of numbers
			nums = []
			for i in range(int(num)):
				nums.append(i)

			return render_to_response(
				'add_classes.html',
				{'user_to_add':user_to_add,
				'nums':nums,
				'total':total,
				'user_to_add_id':user_to_add_id},
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


def class_process(request):
	# Get request's context
	context = RequestContext(request)

	# Get HTTP POST total number of classes to add
	total = int(request.POST.get('total'))

	# ... and the User we are working with
	user_to_add_id = int(request.POST.get('user_to_add_id'))

	# Now, for each class to add, check to see if it is already
	# stored. If not, create a new class/department object. If it
	# is, create a tutor class object.
	for i in range(0,int(total)):
		
		# Get the HTTP POST objects for this particular class
		class_to_add = request.POST.get('class_' + str(i))
		department_to_add = request.POST.get('department_' + str(i))
		number_to_add = request.POST.get('number_' + str(i))

		# First check to see if the department exists
		departments = Department.objects.all()
		dept_id = None

		for dept in departments:
			if dept.name == department_to_add:
				dept_id = dept.id


		tutor_to_associate = None

		for tutor in TutorProfile.objects.all():
			if tutor.user.id == user_to_add_id:
				tutor_to_associate = tutor

		# If no department id was returned in the above, add it...
		if dept_id == None:
			new_department = Department(name=str(department_to_add),
				short_ident = str(department_to_add)[0:4].upper(),
				school=tutor_to_associate.school)
			new_department.save()
			dept_id = new_department.id

		# Now check to see if the class exists
		classes = Class.objects.all()
		class_id = None

		for cl in classes:
			if cl.number == int(number_to_add):
				class_id = cl.id

		# If no class id was returned in the above, add it...
		if class_id == None:
			new_class = Class(department=Department.objects.get(id=dept_id),
				title = str(class_to_add),
				number = int(number_to_add))
			new_class.save()
			class_id = new_class.id

		if tutor_to_associate == None:
			return HttpResponse("This tutor does not exist!!!!")

		# Get the right class to associate
		class_to_associate = Class.objects.get(id=class_id)

		# Construct new tutor class object
		new_tutor_class = TutorClass(
			tutor=tutor_to_associate,
			teach=class_to_associate)

		# Save this tutor class to the database
		new_tutor_class.save()

	return HttpResponse("All things added successfully!")





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
