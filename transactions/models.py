from django.db import models

from core import settings
from customers.models import Orders
from products.models import PlanProducts
from util.django_ext.models import TimeStampMixin

from customers.models import Profile, CustomerCards


# Create your models here.
class TransactionManager(models.Manager):
    def create_transaction(self, order: Orders, **kwargs):
        currency = 'PY'
        try:
            card = order.profile.customercards_set.exclude(alias_token__isnull=True, is_default=False).first()
            amount = int(order.product_plan.plan.price) if card.card_type == 'credit' else int(
                order.product_plan.plan.fee_amount)

            number_of_payments = order.product_plan.plan.installments if card.card_type == 'debit' else 1

            new_transaction = super().create(amount=amount, currency=currency, number_of_payments=number_of_payments,
                                             card=card,
                                             order=order)
        except CustomerCards.DoesNotExist:
            raise Exception('Customer don\'t have a default card. First add a card and set it as default')

        return new_transaction

    def update_transaction(self, **kwargs):
        pass


class Transaction(TimeStampMixin):
    amount = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    currency = models.CharField(max_length=4)
    number_of_payments = models.IntegerField(default=1)
    additional_data = models.CharField(max_length=100, null=True, blank=True)
    preauthorization = models.CharField(max_length=2, default="S")
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
    card = models.ForeignKey(CustomerCards, on_delete=models.DO_NOTHING)

    objects = TransactionManager()

    class Meta:
        db_table = 'transactions'

    def __str__(self):
        return f'{self.id} - {self.authorization_number}'
