from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from customers.models import Profile, Orders, CustomerCards, User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'company_name',
            'street_address',
            'city_name',
            'phone',
            'email_address',
            'is_api_user'
        ]


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email_address')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('id', 'first_name', 'last_name', 'phone', 'email_address')
    list_per_page = 25
    form = ProfileForm


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'product_plan', 'order_code')
    list_display_links = ('id', 'profile', 'product_plan')
    search_fields = ('id', 'order_code', 'profile', 'product_plan')
    list_per_page = 25


class CustomerCardsAdmin(admin.ModelAdmin):
    list_display = ('id', 'card_masked_number', 'expiration_date', 'customer')
    list_display_links = ('id', 'card_masked_number', 'customer')
    search_fields = ('id', 'customer', 'card_masked_number')
    list_per_page = 25


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Orders, OrderAdmin)
admin.site.register(CustomerCards, CustomerCardsAdmin)
