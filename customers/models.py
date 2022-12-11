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
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    product_plan = models.ForeignKey(PlanProducts, related_name="product_plan", on_delete=models.DO_NOTHING)
