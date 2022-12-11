from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout', views.checkout, name='checkout'),
    path('checkout/order-pay/<str:code>', views.order_pay, name='order_pay')
]
