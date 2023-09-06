from rest_framework import serializers

from data_providers.bancard.request import BancardAPI
from .models import Profile, CustomerCards


class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    company_name = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)
    street_address = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    city_name = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    phone = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    email_address = serializers.EmailField(max_length=100, allow_null=True, allow_blank=True)
    user_id = serializers.IntegerField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = '__all__'

    def validate_email_address(self, email_address):
        if Profile.objects.filter(email_address=email_address).exists():
            raise serializers.ValidationError('Email already exists', code='email_exists')
        return email_address


class CardSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    class Meta:
        model = CustomerCards
        fields = ('id', 'customer_id')

    def create_new_card(self):
        try:
            customer = Profile.objects.get(pk=self.validated_data['customer_id'])
            customer_card = CustomerCards.objects.create(customer=customer)

            response = BancardAPI().cards_new(
                card_id=customer_card.id,
                user_id=customer.id,
                phone_number=customer.phone,
                email_addr=customer.email_address
            )

            if response:
                response_json = response.json()
                process_id = response_json['process_id']
                return process_id
            else:
                raise serializers.ValidationError('Error creating card')
        except Profile.DoesNotExist:
            raise serializers.ValidationError('Customer does not exist')


    def update_alias_token(self, card_id):
        try:
            card_data = CustomerCards.objects.get(pk=card_id)
            if card_data:
                card_data.update_alias_token()
                return card_data.alias_token
        except CustomerCards.DoesNotExist:
            raise serializers.ValidationError('Card does not exist')