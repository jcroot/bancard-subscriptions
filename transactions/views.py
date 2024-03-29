from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import Orders
from transactions.models import Transaction
from .serializers import TransactionSerializer, OrderSerializer, OrderListSerializer, TransactionSummarySerializer


# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, order__order_code=self.kwargs['pk'], response_code__isnull=False)
        serializer = self.get_serializer(obj, {'order_code': obj.order.order_code})
        return Response(serializer.data)

    def get_queryset(self):
        return Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.create_order()
            return Response({
                'order_code': transaction.order.order_code,
                'description': transaction.response_description,
                'status': "success" if transaction.response == "S" else "error"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                'order_code': order.order_code
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersViewSet(viewsets.ModelViewSet):
    serializer_class = OrderListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(Orders, order_code=self.kwargs['pk'])
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def get_queryset(self):
        return Orders.objects.all()
