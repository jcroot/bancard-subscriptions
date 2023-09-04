from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import Orders
from transactions.models import Transaction
from .serializers import TransactionSerializer, OrderSerializer, OrderListSerializer


# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        order_code = request.data.get('order_code')


class CheckoutViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.create_order()
            return Response({
                'order_code': order.order_code,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersViewSet(viewsets.ModelViewSet):
    serializer_class = OrderListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, order_code=self.kwargs['pk'])
        return obj
