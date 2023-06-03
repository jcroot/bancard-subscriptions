from django.shortcuts import render
from rest_framework import viewsets

from .models import Plan, Category, Product, PlanProducts
from .serializers import PlanSerializer, CategorySerializer, ProductSerializer, PlanProductSerializer


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer

    def get_queryset(self):
        return Plan.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class PlanProductViewSet(viewsets.ModelViewSet):
    serializer_class = PlanProductSerializer

    def get_queryset(self):
        return PlanProducts.objects.all()
