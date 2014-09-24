from django.db import models
from users.models import UserProfile, TutorProfile
from classes.models import Class
from schools.models import School
import datetime

class Session(models.Model):
	user = models.ForeignKey(UserProfile)
	tutor = models.ForeignKey(TutorProfile)
	teach = models.ForeignKey(Class)
	school = models.ForeignKey(School)
	start_time = models.DateTimeField(auto_now=False)
	end_time = models.DateTimeField(auto_now=False)
