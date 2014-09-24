from django.contrib import admin
from calls.models import Call

class CallAdmin(admin.ModelAdmin):
	list_display = ('teach', 'start_time', 'active')

admin.site.register(Call, CallAdmin)
# Register your models here.
