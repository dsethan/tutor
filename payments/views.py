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
from payments.models import CustomerToken
import stripe


def process_new_card(request):
	# Get request's context
	context = RequestContext(request)

	# Stripe API Key (make sure to change this)
	stripe.api_key = "sk_test_gii6sAzH4fvDd6xCENhAgb9j"

	# If POST, add the right user
	if request.method == "POST":

		# Get the appropriate values from the form
		token = request.POST['stripeToken']
		user_id = request.POST.get('user_to_add')
		user = User.objects.get(id=user_id)

		print user
		# Create customer on Stripe's servers
		customer = stripe.Customer.create(
			card = token,
			description = user
		)

		# Save token info into our database for future use
		cust_token_to_add = CustomerToken(
			customer = user,
			token = token,
			default = True
			)

		# Save new customer token to the database
		cust_token_to_add.save()

		return redirect('/student', user=user)

	return HttpResponse("Error.")