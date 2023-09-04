from rest_framework import routers
from django.urls import include, path

from customers.views import CustomerViewSet, CardNewViewSet
from products.views import PlanViewSet, CategoryViewSet, ProductViewSet, PlanProductViewSet
from transactions.views import TransactionViewSet, CheckoutViewSet, OrdersViewSet

PREFIX = "api"

router = routers.DefaultRouter()
router.register(r'confirm', TransactionViewSet, 'transactions')
router.register(r'checkout', CheckoutViewSet, 'checkout')
router.register(r'orders', OrdersViewSet, 'orders')
router.register(r'profile', CustomerViewSet, 'profile')
router.register(r'plan', PlanViewSet, 'plan')
router.register(r'category', CategoryViewSet, 'category')
router.register(r'product', ProductViewSet, 'product')
router.register(r'plan_products', PlanProductViewSet, 'plan_products')
router.register(r'card_new', CardNewViewSet, 'card_new')

urlpatterns = [
    path(f"{PREFIX}/", include(router.urls)),
]
