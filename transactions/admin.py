from django import forms
from django.contrib import admin

from transactions.models import Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'response')
    list_display_links = ('id', 'order')
    search_fields = ('order', 'response')
    list_per_page = 25

admin.site.register(Transaction, TransactionAdmin)