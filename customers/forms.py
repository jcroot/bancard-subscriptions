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
            "email_address",
        )

    def save(self, commit=True):
        profile = super(CustomerForm, self).save(commit=False)
        profile.email_address = self.cleaned_data['email_address']
        profile.user_id = self.cleaned_data['user_id']
        if commit:
            profile.save()
        return profile