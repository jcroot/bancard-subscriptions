from rest_framework import serializers

from data_providers.bancard.request import BancardAPI
from .models import Profile, CustomerCards


class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    company_name = serializers.CharField(max_length=100, allow_blank=True)
    street_address = serializers.CharField(max_length=255)
    city_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=50)
    email_address = serializers.EmailField(max_length=100)

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'street_address',
                  'city_name', 'phone', 'email_address', 'company_name')

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
