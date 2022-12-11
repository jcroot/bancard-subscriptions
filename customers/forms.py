from django import forms

from .models import Profile


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "street_address",
            "city_name",
            "phone",
            "email_address"
        )
