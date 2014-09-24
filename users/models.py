from django.db import models
from django.contrib.auth.models import User
from datetime import date, time, timedelta
from schools.models import School


class UserProfile(models.Model):
	# User object associated to this UserProfile
	user = models.OneToOneField(User)

	# Get related school object for this UserProfile
	# TODO: Implement the School model
	school = models.ForeignKey(School)

	# Phone number
	phone = models.IntegerField(max_length=11)
	
	def __unicode__(self):
		return self.user.username

class TutorProfile(models.Model):
	# User object associated to this TutorProfile
	user = models.OneToOneField(User)

	# Get related school object for this UserProfile
	school = models.ForeignKey(School)

	# Phone number
	phone = models.IntegerField(max_length=11)

	# Is currently active
	active = models.BooleanField(default=True)

	def is_active(self):
		return self.active

	def __unicode__(self):
		return self.user.username