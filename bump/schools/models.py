from django.db import models

class School(models.Model):
	# Name of the school (including 'University', 'College', etc.)
	school = models.CharField(max_length=40)

	# Localization information
	city = models.CharField(max_length=40)

	# Two letter abbreviation of the state required
	state = models.CharField(max_length=2)

	def __unicode__(self):
		return str(self.school)