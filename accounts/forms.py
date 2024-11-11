# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')  # Add any additional fields you want in the signup form

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Add CSS classes and ensure id and name attributes are set
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'username',  # Custom id
            'name': 'username'  # Custom name
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'email',  # Custom id
            'name': 'email'  # Custom name
        })
        self.fields['role'].widget.attrs.update({
            'class': 'form-control',
            'id': 'role',  # Custom id
            'name': 'role'  # Custom name
        })

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')  # Add any additional fields you want in the user edit form

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        # Add CSS classes and ensure id and name attributes are set
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'username',  # Custom id
            'name': 'username'  # Custom name
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'email',  # Custom id
            'name': 'email'  # Custom name
        })
        self.fields['role'].widget.attrs.update({
            'class': 'form-control',
            'id': 'role',  # Custom id
            'name': 'role'  # Custom name
        })