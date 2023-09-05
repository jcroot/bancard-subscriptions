from rest_framework import serializers

from customers.models import CustomerCards, Orders, Profile
from customers.serializers import CustomerSerializer
from data_providers.bancard.request import BancardAPI
from products.models import PlanProducts
from products.serializers import PlanProductSerializer
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    order_code = serializers.CharField(max_length=20)

    class Meta:
        model = Transaction
        fields = ('order_code',)

    def validate_order_code(self, order_code):
        self.order_code = order_code
        if not Orders.objects.filter(order_code=order_code).exists():
            return serializers.ValidationError('Order does not exist')

        return order_code

    def create_order(self):
        order = Orders.objects.get(order_code=self.order_code)
        try:
            customer_card = CustomerCards.objects.get(customer_id=order.profile.id,
                                                      customer__customercards__is_default=True)

            response = BancardAPI().charge(shop_process_id=order.id,
                                           amount=order.product_plan.price,
                                           description=order.product_plan.plan.title_plan,
                                           alias_token=customer_card.alias_token,
                                           number_of_payments=order.product_plan.plan.number_of_payments)

            response_json = response.json()

        except CustomerCards.DoesNotExist:
            raise serializers.ValidationError(
                'Customer don\'t have a default card. First add a card and set it as default')
        return order


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
