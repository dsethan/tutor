from django.contrib import admin
from payments.models import CustomerToken

class CustomerTokenAdmin(admin.ModelAdmin):
	list_display = ('customer', 'token', 'default')

admin.site.register(CustomerToken, CustomerTokenAdmin)