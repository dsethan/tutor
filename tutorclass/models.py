from django.db import models
from users.models import TutorProfile
from classes.models import Class

class TutorClass(models.Model):
	tutor = models.ForeignKey(TutorProfile)
	teach = models.ForeignKey(Class)