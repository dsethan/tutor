from django.db import models
from classes.models import Class
import datetime

class Call(models.Model):
	# Get associated class information
	teach = models.ForeignKey(Class)

	# Get request time
	start_time = models.DateTimeField(auto_now=True)

	# Is call active?
	active = models.BooleanField(default=True)

	def is_active(self):
		return self.active