from django.db import models

from customers.models import Orders
from util.django_ext.models import TimeStampMixin

from customers.models import Profile, CustomerCards

# Create your models here.
class Transaction(TimeStampMixin):
    amount = models.DecimalField(decimal_places=2, default=0, max_digits=6)
    currency = models.CharField(max_length=4)
    number_of_payments = models.IntegerField(default=1)
    additional_data = models.CharField(max_length=100, null=True, blank=True)
    preauthorization = models.CharField(max_length=2,default="S")
    response = models.CharField(max_length=2, null=True, blank=True)
    response_details = models.CharField(max_length=50, null=True, blank=True)
    authorization_number = models.CharField(max_length=50, null=True, blank=True)
    ticket_number = models.CharField(max_length=50, null=True, blank=True)
    iva_amount = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    iva_ticket_number = models.CharField(max_length=50, blank=True, null=True)
    response_code = models.CharField(max_length=50, blank=True, null=True)
    response_description = models.CharField(max_length=50, null=True, blank=True)
    security_information = models.CharField(max_length=255, null=True, blank=True)

    order = models.ForeignKey(Orders, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.id} - {self.authorization_number}'


class Charge(TimeStampMixin):
    amount = models.DecimalField(decimal_places=2, default=0, max_digits=6)
    number_of_payments = models.IntegerField(default=1)
    card = models.ForeignKey(CustomerCards, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
