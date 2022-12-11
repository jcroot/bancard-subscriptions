from django.contrib import admin

from customers.models import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email_address')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('id', 'first_name', 'last_name', 'phone', 'email_address')
    list_per_page = 25


admin.site.register(Profile, ProfileAdmin)
