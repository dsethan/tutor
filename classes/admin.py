from django.contrib import admin
from classes.models import Class

class ClassAdmin(admin.ModelAdmin):
	list_display = ('department', 'title', 'number')

admin.site.register(Class, ClassAdmin)
# Register your models here.
