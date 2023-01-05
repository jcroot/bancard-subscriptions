from django.urls import path

from core import api_urls
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/<str:code>', views.checkout, name='checkout'),
    path('checkout/order-pay/<str:code>', views.order_pay, name='order_pay'),
    path('cards/confirm/<str:user_id>', views.card_return_url, name='card_return_url'),
    path('add-item', views.add_item_to_cart, name='add_item'),
]
