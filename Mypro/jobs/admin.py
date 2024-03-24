from django.contrib import admin
from jobs.models import *
# Register your models here.
admin.site.register(JobListing)
admin.site.register(CompanyProfile)
admin.site.register(Profile)
admin.site.register(JobApplication)

