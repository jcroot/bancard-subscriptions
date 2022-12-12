import uuid

from django.db import models

from products.models import PlanProducts


# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=255)
    city_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email_address = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Orders(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = "Orders"

    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    product_plan = models.ForeignKey(PlanProducts, related_name="product_plan", on_delete=models.DO_NOTHING)
    order_code = models.CharField(max_length=50, default=uuid.uuid4().hex[:8].upper())

    def __str__(self):
        return self.order_code


class CustomerCards(models.Model):
    class Meta:
        verbose_name = 'Customer Card'
        verbose_name_plural = "Customer Cards"

    alias_token = models.CharField(max_length=100, null=True, blank=True)
    card_masked_number = models.CharField(max_length=20, null=True, blank=True)
    expiration_date = models.CharField(max_length=10, null=True, blank=True)
    card_brand = models.CharField(max_length=100, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    card_type = models.CharField(max_length=20, null=True, blank=True)

    customer = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.card_masked_number} - {self.expiration_date}'


class CartManager(models.Manager):
    def create_cart(self, product_plan):
        session_code = self.get_unique_id()
        cart = super().create(session_code=session_code, product_plan=product_plan)

        return cart

    def get_unique_id(self):
        session_code = uuid.uuid4().hex[:8].upper()
        while Cart.objects.filter(session_code=session_code).exists():
            session_code = uuid.uuid4().hex[:8].upper()
        return session_code


class Cart(models.Model):
    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ('-creation_date',)

    creation_date = models.DateTimeField(verbose_name='creation date', auto_now_add=True)
    checked_out = models.BooleanField(default=False, verbose_name='checked out')
    session_code = models.CharField(max_length=50)
    product_plan = models.ForeignKey(PlanProducts, related_name="cart_plan", on_delete=models.DO_NOTHING)

    objects = CartManager()

    def __unicode__(self):
        return self.creation_date

    def __str__(self):
        return self.session_code

