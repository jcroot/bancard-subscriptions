from rest_framework import serializers

from customers.models import CustomerCards, Orders, Profile
from customers.serializers import CustomerSerializer
from products.models import PlanProducts
from products.serializers import PlanProductSerializer
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    alias_token = serializers.CharField(max_length=255)
    order = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = ('id', 'number_of_payments')

    def validate(self, attrs):
        if 'number_of_payments' in attrs:
            if attrs['number_of_payments'] < 1:
                raise serializers.ValidationError('Number of payments must be greater than 0')

    def validate_alias_token(self, alias_token):
        if not CustomerCards.objects.filter(alias_token=alias_token).exists():
            return serializers.ValidationError('Card does not exist')

    def validate_order(self, order_id):
        if not Orders.objects.filter(id=order_id).exists():
            return serializers.ValidationError('Order does not exist')

        return order_id


class OrderSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    product_plan_id = serializers.IntegerField()

    class Meta:
        model = Orders
        fields = ['customer_id', 'product_plan_id']

    def create_order(self):
        customer = Profile.objects.get(pk=self.customer_id)
        product_plan = PlanProducts.objects.get(pk=self.product_plan_id)

        order = Orders.objects.create_order(profile=customer, product_plan=product_plan)

        return order

    def validate_customer_id(self, customer_id):
        self.customer_id = customer_id
        if not Profile.objects.filter(id=customer_id).exists():
            raise serializers.ValidationError('Customer does not exist')
        return self.customer_id

    def validate_product_plan_id(self, product_plan_id):
        self.product_plan_id = product_plan_id
        if not PlanProducts.objects.filter(id=product_plan_id).exists():
            raise serializers.ValidationError('Product plan does not exist')
        return self.product_plan_id


class OrderListSerializer(serializers.ModelSerializer):
    profile = CustomerSerializer(read_only=True, )
    product_plan = PlanProductSerializer(read_only=True, )

    class Meta:
        model = Orders
        fields = ['id', 'order_code', 'profile', 'product_plan']
