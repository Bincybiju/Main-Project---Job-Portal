import re
from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class JobSeekerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [ 'username', 'email', 'password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("Password is required")
        # Password regex pattern
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@])[A-Za-z\d@]{8,}$'
        # Check if password matches the pattern
        if not re.match(pattern, password):
            raise ValidationError("Password must contain at least one uppercase letter, one lowercase letter, one digit, and one '@'")
        return password

class EmployerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name' ,'username', 'email', 'phone_number', 'gender', 'address',  'password1','password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Validate phone number length
        if len(phone_number) < 10:
            raise ValidationError("Phone number must be at least 10 characters long")
        return phone_number
    
    

