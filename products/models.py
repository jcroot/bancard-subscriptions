from django.db import models


# Create your models here.
class Plan(models.Model):
    title_plan = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0)

    def __str__(self):
        return self.title_plan


class Category(models.Model):
    title_category = models.CharField(max_length=200)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title_category


class Product(models.Model):
    title_product = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_product = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title_product


class PlanProducts(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
