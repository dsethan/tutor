from django.db import models
from departments.models import Department

class Class(models.Model):
	department = models.ForeignKey(Department)
	title = models.CharField(max_length=100)
	number = models.IntegerField()

	def __unicode__(self):
		return str(self.title)