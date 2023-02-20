import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser, User
from django.db import models
from django.utils.translation import gettext as _

from core import settings
from products.models import PlanProducts
from data_providers.bancard.request import BancardAPI


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class UserProfile(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=255)
    city_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email_address = models.CharField(max_length=100)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def check_if_had_alias_token(self):
        response = BancardAPI().users_cards(self.id)
        if response:
            response_json = response.json()
            if response_json['status'] == 'success' and len(response_json['cards']) > 0:
                for card in response_json['cards']:
                    card_customer, created = CustomerCards.objects.get_or_create(
                        card_masked_number=card['card_masked_number'],
                        expiration_date=card['expiration_date'],
                        card_brand=card['card_brand'],
                        card_type=card['card_type'],
                        customer_id=self.id
                    )

                    if card_customer:
                        card_customer.alias_token = card['alias_token']


class OrderManager(models.Manager):
    def create_order(self, profile, product_plan):
        order_code = self.get_unique_id()
        order = self.check_if_not_duplicate(profile=profile, product_plan=product_plan)
        if not order:
            order = super().create(order_code=order_code, profile=profile, product_plan=product_plan)

        return order

    def get_unique_id(self):
        session_code = uuid.uuid4().hex[:8].upper()
        while Cart.objects.filter(session_code=session_code).exists():
            session_code = uuid.uuid4().hex[:8].upper()
        return session_code

    def check_if_not_duplicate(self, profile, product_plan):
        return super().filter(profile=profile, product_plan=product_plan).first()


class Orders(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    product_plan = models.ForeignKey(PlanProducts, related_name="product_plan", on_delete=models.DO_NOTHING)
    order_code = models.CharField(max_length=50)

    objects = OrderManager()

    def __str__(self):
        return self.order_code


class CustomerCards(models.Model):
    class Meta:
        verbose_name = _('Customer Card')
        verbose_name_plural = _('Customer Cards')

    alias_token = models.CharField(max_length=100, null=True, blank=True)
    card_masked_number = models.CharField(max_length=20, null=True, blank=True)
    expiration_date = models.CharField(max_length=10, null=True, blank=True)
    card_brand = models.CharField(max_length=100, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    card_type = models.CharField(max_length=20, null=True, blank=True)
    card_is_deleted = models.BooleanField(default=False)

    customer = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.customer.first_name} {self.customer.last_name} - {self.card_masked_number} - {self.expiration_date}'

    def update_alias_token(self):
        response = BancardAPI().users_cards(self.customer_id)
        if response:
            response_json = response.json()
            if response_json['status'] == 'success':
                if len(response_json['cards']) > 0:
                    for card in response_json['cards']:
                        try:
                            card_customer = CustomerCards.objects.get(pk=card['card_id'])
                            if not card_customer.card_is_deleted:
                                card_customer.alias_token = card['alias_token']
                                card_customer.card_masked_number = card['card_masked_number']
                                card_customer.expiration_date = card['expiration_date']
                                card_customer.card_brand = card['card_brand']
                                card_customer.card_type = card['card_type']
                                card_customer.save(update_fields=['alias_token', 'card_masked_number',
                                                                  'expiration_date', 'card_brand', 'card_type'])

                        except CustomerCards.DoesNotExist:
                                card_customer = None

                else:
                    self.alias_token = None
                    self.is_default = False
                    self.card_is_deleted = True
                    self.save(update_fields=['alias_token', 'is_default'])


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
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
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
