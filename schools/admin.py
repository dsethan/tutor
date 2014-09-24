from django.contrib import admin
from schools.models import School

class SchoolAdmin(admin.ModelAdmin):
	list_display = ('school', 'city', 'state')

admin.site.register(School, SchoolAdmin)
# Register your models here.
