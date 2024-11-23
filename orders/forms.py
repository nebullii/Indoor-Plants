from django import forms
from .models import ShippingAddress
from django_countries.widgets import CountrySelectWidget
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'address', 'city', 'state', 'postal_code', 'phone_number', 'country']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '5-digit postal code',
                'maxlength': '5'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
                'pattern': '[0-9]{10}',
                'title': 'Please enter a valid 10-digit phone number'
            }),
            'country': CountrySelectWidget(attrs={
                'class': 'form-control',
            }),
        }


    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # Remove any non-digit characters
        phone = ''.join(filter(str.isdigit, phone))
        if len(phone) != 10:
            raise forms.ValidationError('Please enter a valid 10-digit phone number')
        # Format phone number as XXX-XXX-XXXX
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"

    def clean_postal_code(self):
        postal = self.cleaned_data.get('postal_code')
        if not postal.isdigit() or len(postal) != 5:
            raise forms.ValidationError('Please enter a valid 5-digit ZIP code')
        return postal

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name')
        if len(name.split()) < 2:
            raise forms.ValidationError('Please enter both first and last name')
        return name.title()  # Capitalize first letter of each word