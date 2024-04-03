# urls.py
from django.urls import path
from .views import *
from .import views
from django.conf.urls.static import static


urlpatterns = [
    path('create_or_edit_company_profile/', views.create_or_edit_company_profile, name='create_or_edit_company_profile'),
    path('create_job_listing/', views.create_job_listing, name='create_job_listing'),
    path('edit_job/', views.edit_job, name='edit_job'),
    path('edit_job_listing/<int:job_id>/', views.edit_job_listing, name='edit_job_listing'),
    path('delete_job/', views.delete_job, name='delete_job'),
    path('delete_job_listing/<int:job_id>/', views.delete_job_listing, name='delete_job_listing'),
    path('job_listings/', views.job_listings, name='job_listings'),
    path('logout/', views.logout, name='logout'),
    path('manage_accounts/', views.manage_accounts, name='manage_accounts'),
    path('admin_profile/', admin_profile, name='admin_profile'),
    path('view_employer_profile/<int:employer_id>/', view_employer_profile, name='view_employer_profile'),
    path('delete_employer_account/<int:employer_id>/', delete_employer_account, name='delete_employer_account'),
    path('manage_job_listings/', manage_job_listings, name='manage_job_listings'),
    path('company_jobs/<int:company_id>/', company_jobs, name='company_jobs'),
    path('delete_jobs/<int:job_id>/', delete_jobs, name='delete_jobs'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search/', search_jobs, name='search_jobs'),
    path('job/<int:job_id>/', views.job_details, name='job_details'), 
    path('apply_jobs/', apply_jobs, name='apply_jobs'),
    path('submit_job/<int:job_id>/', submit_job, name='submit_job'),
    path('manage_job_applications/', views.manage_job_applications, name='manage_job_applications'),
    path('view_job_seeker_profile/<int:user_id>/', views.view_job_seeker_profile, name='view_job_seeker_profile'),
    path('update_application_status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('applied-jobs/', applied_jobs_status, name='applied_jobs_status'),
    path('view_reports/', view_reports, name='view_reports'),
    path('report_issue/', report_issue, name='report_issue'),
    path('reported_issues/', reported_issues, name='reported_issues'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
