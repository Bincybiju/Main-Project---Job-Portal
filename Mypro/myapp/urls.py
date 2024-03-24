from django.urls import path
from .import views
from .views import *
urlpatterns = [
    path('index/', views.index,name='index'),
    path('employer/', views.employer, name='employer'),
    path('job_seeker/', views.job_seeker, name='job_seeker'),
    path('employer_profile/', views.employer_profile, name='employer_profile'),
    path('jobseeker_profile/', views.jobseeker_profile, name='jobseeker_profile'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('login_view/', views.login_view , name='login_view'),
]