from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'number_of_payments')


    def validate(self, attrs):
        if 'number_of_payments' in attrs:
            if attrs['number_of_payments'] < 1:
                raise serializers.ValidationError('Number of payments must be greater than 0')

        