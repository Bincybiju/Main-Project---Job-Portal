from django import forms
from .models import *

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'industry', 'location', 'website', 'description']

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        exclude = ['company', 'created_at']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'resume', 'skills', 'degree', 'degree_percentage']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cv', 'cover_letter', 'experience']

