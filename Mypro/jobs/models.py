from django.db import models
from django.conf import settings
from myapp.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class CompanyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=0)
    company_name = models.CharField(max_length=100,default=0)
    industry = models.CharField(max_length=100,default=0)
    location = models.CharField(max_length=100,default=0)
    website = models.URLField(default=0)
    description = models.TextField(default=0)

class JobListing(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_qualifications = models.TextField()
    desired_qualifications = models.TextField()
    responsibilities = models.TextField()
    application_deadline = models.DateField()
    salary_range = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50)
    company_benefits = models.TextField()
    how_to_apply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=0)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes/')
    skills = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    degree_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

class JobApplication(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey('JobListing', on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cv/')
    cover_letter = models.TextField()
    experience = models.IntegerField(default=0)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

