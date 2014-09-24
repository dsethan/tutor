from django.contrib import admin
from tutorclass.models import TutorClass

class TutorClassAdmin(admin.ModelAdmin):
	list_display = ('tutor', 'teach')

admin.site.register(TutorClass, TutorClassAdmin)
# Register your models here.
