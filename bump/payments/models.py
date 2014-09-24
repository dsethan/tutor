from django.db import models
from users.models import UserProfile
from django.contrib.auth.models import User

class CustomerToken(models.Model):
	customer = models.ForeignKey(User)
	token = models.CharField(max_length=50)
	default = models.BooleanField(default=True)