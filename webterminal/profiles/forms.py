from django import forms
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    send_contact_reminders = forms.BooleanField(required=False)
    send_birthday_reminders = forms.BooleanField(required=False)
    check_twitter_dms = forms.BooleanField(required=False)
    check_foursquare = forms.BooleanField(required=False)
    #phone_number = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']