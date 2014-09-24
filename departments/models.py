from django.db import models
from schools.models import School

# Create your models here.

class Department(models.Model):
	name = models.CharField(max_length=100)
	short_ident = models.CharField(max_length=4)
	school = models.ForeignKey(School)

	def __unicode__(self):
		return str(self.name)