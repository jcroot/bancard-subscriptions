from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from transactions.models import Transaction
from .serializers import TransactionSerializer
from rest_framework.response import Response


# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all()
