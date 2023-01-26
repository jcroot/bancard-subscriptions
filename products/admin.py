from django.contrib import admin

from .models import Product, PlanProducts, Plan, Category


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_product', 'category')
    list_display_links = ('id', 'title_product')
    search_fields = ('id','title_product')
    list_per_page = 25

    def delete_model(self, request, obj):
        print("entre")


class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_plan', 'price', 'installments')
    list_display_links = ('id', 'title_plan')
    search_fields = ('id', 'title_plan', 'price')
    list_per_page = 25


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_category')
    list_display_links = ('id', 'title_category')
    search_fields = ('id', 'title_category')
    list_per_page = 25


class PlanProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan', 'product')
    list_display_links = ('id', 'plan', 'product')
    search_fields = ('plan', 'product')
    list_per_page = 25


admin.site.register(Product, ProductAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PlanProducts, PlanProductAdmin)
