from django.contrib import admin
from departments.models import Department

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('name', 'short_ident')

admin.site.register(Department, DepartmentAdmin)
# Register your models here.
