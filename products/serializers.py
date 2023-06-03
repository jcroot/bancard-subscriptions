from rest_framework import serializers

from .models import Plan, Category, Product, PlanProducts


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PlanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanProducts
        fields = '__all__'
