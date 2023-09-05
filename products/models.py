from django.db import models


# Create your models here.
class Plan(models.Model):
    title_plan = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    installments = models.SmallIntegerField(default=1)
    fee_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f'{self.title_plan} - Gs. {self.price}'


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title_category = models.CharField(max_length=200)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title_category


class Product(models.Model):
    title_product = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_product = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.title_product


class PlanProducts(models.Model):
    class Meta:
        verbose_name = "Product Plan"
        verbose_name_plural = "Product Plans"

    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.plan.title_plan} - {self.product.title_product} ({self.plan.price})'
