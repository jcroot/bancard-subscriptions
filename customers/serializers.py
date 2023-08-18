from rest_framework import serializers

from .models import Profile, CustomerCards


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'company_name', 'street_address',
                  'city_name', 'phone', 'email_address', 'user')


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCards
        fields = ('id', 'customer')

    def create(self, validated_data):
        if 'customer_id' in validated_data:
            customer_id = validated_data['customer']
            customer = Profile.objects.get(pk=customer_id)
            card = CustomerCards.objects.create(customer=customer)
            return card
