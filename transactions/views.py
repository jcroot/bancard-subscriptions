from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from transactions.models import Transaction
from .serializers import TransactionSerializer
from rest_framework.response import Response


# Create your views here.
class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    def list(self, request):
        queryset = Transaction.objects.all()
        serializer = TransactionSerializer(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Transaction.objects.all()
        transaction = get_object_or_404(queryset, pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def create(self, request):
        data = {
            "status": "success",
            "message": "Create row uccessfully"
        }
        return Response(data=data)

    def update(self, request, pk=None):
        data = {
            "status": "success",
            "message": "Update row successfully"
        }
        return Response(data=data)