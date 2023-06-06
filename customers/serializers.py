from rest_framework import serializers

from .models import Profile


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'company_name', 'street_address',
                  'city_name', 'phone', 'email_address', 'user')

