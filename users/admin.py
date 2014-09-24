from django.contrib import admin
from users.models import UserProfile, TutorProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'school', 'phone')

class TutorProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'school', 'phone')
	
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(TutorProfile, TutorProfileAdmin)
