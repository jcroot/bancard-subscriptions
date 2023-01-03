from django import forms
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

from transactions.models import Transaction, Charge


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        exclude = ('status', 'amount', 'number_of_payments')


# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'response')
    list_display_links = ('id', 'order')
    search_fields = ('order', 'response')
    list_per_page = 25

class ChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'amount', 'created_at', 'status')
    list_display_links = ('id', 'card')
    search_fields = ('card__customer_cards', 'status')
    list_per_page = 25
    form = ChargeForm
    add_form_template = "admin/charge_add.html"


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Charge, ChargeAdmin)