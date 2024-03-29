from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/<str:code>', views.checkout, name='checkout'),
    path('checkout/order-pay/<str:code>', views.order_pay, name='order-pay'),
    path('cards/confirm/<str:card_id>', views.card_return_url, name='card-return_url'),
    path('add-item', views.add_item_to_cart, name='add_item'),
    path('customer/', include('customers.urls'))
]
