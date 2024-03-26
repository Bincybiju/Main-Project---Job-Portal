from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from myapp.models import CustomUser
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

@login_required
def create_or_edit_company_profile(request):
    try:
        # Try to retrieve the existing company profile for the current user
        profile = request.user.companyprofile
        editing = True
    except CompanyProfile.DoesNotExist:
        # If the company profile does not exist, set profile to None
        profile = None
        editing = False

    if request.method == 'POST':
        # If it's a POST request, initialize the form with the profile data if exists
        form = CompanyProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # If the form is valid, save the profile
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            # Redirect to the employer profile page
            return redirect('employer_profile')
    else:
        # If it's a GET request, initialize the form with the profile data if exists
        form = CompanyProfileForm(instance=profile)

    # Render the form template
    return render(request, 'create_cprofile.html', {'form': form, 'editing': editing})

@login_required
def create_job_listing(request):
    # Check if the employer has a company profile
    try:
        # Check if the employer has a company profile
        if not request.user.companyprofile:
            return HttpResponse('<script>alert("Please create a company profile first."); window.location.replace("/create_or_edit_company_profile");</script>')
    except CompanyProfile.DoesNotExist:
        return HttpResponse('<script>alert("Please create a company profile first."); window.location.replace("/create_or_edit_company_profile");</script>')

    if not request.user.companyprofile:
        return redirect('create_or_edit_company_profile')

    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job_listing = form.save(commit=False)
            job_listing.company = request.user.companyprofile
            job_listing.save()
            return redirect('job_listings')
    else:
        form = JobListingForm()
    return render(request, 'create_job_listing.html', {'form': form})


@login_required
def edit_job(request):
    try:
        # Check if the employer has a company profile
        if not request.user.companyprofile:
            return HttpResponse('<script>alert("Please create a company profile first."); window.location.replace("/create_or_edit_company_profile");</script>')
    except CompanyProfile.DoesNotExist:
        return HttpResponse('<script>alert("Please create a company profile first."); window.location.replace("/create_or_edit_company_profile");</script>')

    # Filter job listings based on the logged-in user's company
    job_list = JobListing.objects.filter(company=request.user.companyprofile)
    return render(request, 'edit_job.html', {'job_list': job_list})

@login_required
def edit_job_listing(request, job_id):
    
    job_listing = get_object_or_404(JobListing, pk=job_id)
    
    # Check if the job listing belongs to the logged-in user's company
    if job_listing.company != request.user.companyprofile:
        # If not, redirect the user to the job listings page
        return redirect('job_listings')
    
    if request.method == 'POST':
        form = JobListingForm(request.POST, instance=job_listing)
        if form.is_valid():
            form.save()
            return redirect('job_listings')
    else:
        form = JobListingForm(instance=job_listing)
    return render(request, 'edit_job_listing.html', {'form': form})

@login_required
def delete_job(request):
    try:
        # Check if the employer has a company profile
        if not request.user.companyprofile:
            return HttpResponse('<script>alert("Please create a company profile first."); window.location.replace("/create_or_edit_company_profile");</script>')
    except CompanyProfile.DoesNotExist:
        return HttpResponse('<script>alert("Please create a company profile first."); window.location.replace("/create_or_edit_company_profile");</script>')

    # Filter job listings based on the logged-in user's company
    job_list = JobListing.objects.filter(company=request.user.companyprofile)
    return render(request, 'delete_job.html', {'job_list': job_list})

@login_required
def delete_job_listing(request, job_id):   
    job_listing = get_object_or_404(JobListing, pk=job_id)
    
    # Check if the job listing belongs to the logged-in user's company
    if job_listing.company != request.user.companyprofile:
        # If not, redirect the user to the job listings page
        return redirect('job_listings')
    
    if request.method == 'POST':
        job_listing.delete()
        return redirect('job_listings')
    return render(request, 'delete_job_listing.html', {'job_listing': job_listing})

@login_required
def job_listings(request):
    try:
        # Check if the employer has a company profile
        if not request.user.companyprofile:
            return HttpResponse('<script>alert("Please create a company profile first."); window.location.replace("/create_or_edit_company_profile");</script>')
    except CompanyProfile.DoesNotExist:
        return HttpResponse('<script>alert("Please create a company profile first."); window.location.replace("/create_or_edit_company_profile");</script>')

    # Filter job listings based on the logged-in user's company
    job_list = JobListing.objects.filter(company=request.user.companyprofile)
    return render(request, 'job_listings.html', {'job_list': job_list})


def logout(request):
    return redirect('login_view')



@login_required
def admin_profile(request):
    # Get all registered employers
    registered_employers = User.objects.filter(companyprofile__isnull=False)

    return render(request, 'admin_profile.html', {'registered_employers': registered_employers})

@login_required
def manage_accounts(request):
    # Query all registered employers (CustomUser objects)
    registered_employers = CustomUser.objects.all().filter(user_type='employer')
    return render(request, 'manage_accounts.html', {'registered_employers': registered_employers})

@login_required
def view_employer_profile(request, employer_id):
    # Get the employer's User object
    employer = get_object_or_404(User, id=employer_id)
    
    # Access the associated company profile
    profile = employer.companyprofile
    
    return render(request, 'view_userprofile.html', {'profile': profile})



@login_required
def delete_employer_account(request, employer_id):
    # Get the employer to be deleted
    employer = get_object_or_404(User, id=employer_id)
    
    # Delete the associated company profile (if exists)
    if hasattr(employer, 'companyprofile'):
        employer.companyprofile.delete()

    # Delete the employer's account
    employer.delete()

    return redirect('admin_profile')

@login_required
def manage_job_listings(request):
    # Get all companies
    companies = CompanyProfile.objects.all()
    return render(request, 'manage_job_listing.html', {'companies': companies})

@login_required
def company_jobs(request, company_id):
    try:
        company = CompanyProfile.objects.get(id=company_id)
        jobs = JobListing.objects.filter(company=company)
        return render(request, 'company_jobs.html', {'company': company, 'jobs': jobs})
    except CompanyProfile.DoesNotExist:
        return HttpResponse("Company not found", status=404)
    
@login_required
def delete_jobs(request, job_id):
    job = get_object_or_404(JobListing, pk=job_id)

    # Check if the user has permission to delete the job
    if request.user.is_staff or job.company.user == request.user:
        job.delete()
        return HttpResponse('<script>alert(" Job deleted successfully."); window.location.replace("/manage_job_listings");</script>')
  

@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.profile  # Retrieve the profile associated with the logged-in user
    except Profile.DoesNotExist:
        # If the profile does not exist, create a new one
        profile = Profile(user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('jobseeker_profile')
        else:
            # Form is not valid, render the form again with validation errors
            return render(request, 'edit_profile.html', {'form': form})
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def search_jobs(request):
    keyword = request.GET.get('keyword')
    location = request.GET.get('location')
    company_name = request.GET.get('company_name')

    # Filter job listings based on search parameters
    job_listings = JobListing.objects.all()

    if keyword:
        job_listings = job_listings.filter(title__icontains=keyword)
    if location:
        job_listings = job_listings.filter(location__icontains=location)
    if company_name:
        job_listings = job_listings.filter(company__company_name__icontains=company_name)

    # Optionally, sort search results
    # job_listings = job_listings.order_by('-created_at')  # Example sorting by date

    return render(request, 'search_jobs.html', {'job_listings': job_listings})


@login_required
def job_details(request, job_id):
    job = get_object_or_404(JobListing, pk=job_id)  # Retrieve job details by ID
    return render(request, 'job_details.html', {'job': job})




@login_required
def apply_jobs(request):
    try:
        # Check if the employer has a company profile
        if not request.user.profile:
            return HttpResponse('<script>alert("Please complete your profile first."); window.location.replace("/edit__profile");</script>')
    except Profile.DoesNotExist:
        return HttpResponse('<script>alert("Please complete you profile first."); window.location.replace("/edit_profile");</script>')

    # If the user has a profile, allow them to view the available jobs
    job_listings = JobListing.objects.all()
    return render(request, 'apply_jobs.html', {'job_listings': job_listings})


@login_required
def submit_job(request, job_id):
    if request.user.is_authenticated:
        existing_application = JobApplication.objects.filter(user=request.user, job_id=job_id).exists()
        if existing_application:
            return HttpResponse('<script>alert("You have already applied for this job."); window.location.replace("/apply_jobs");</script>')
        else:
            if request.method == 'POST':
                form = JobApplicationForm(request.POST, request.FILES)
                if form.is_valid():
                    job_application = form.save(commit=False)
                    job_application.user = request.user
                    job_application.job_id = job_id
                    job_application.save()

                    # Send email to job seeker
                    job_seeker_email = request.user.email
                    subject_seeker = 'Job Application Confirmation'
                    message_seeker = f"Dear {request.user.username},\n\nThank you for applying for the job. Your application has been received successfully.\n\nBest regards,\nYour Company Name"
                    send_mail(subject_seeker, message_seeker, 'your@example.com', [job_seeker_email])

                    # Send email to employer
                    employer_email = job_application.job.company.user.email
                    subject_employer = 'New Job Application Received'
                    message_employer = f"Dear Employer,\n\nA new job application has been received for the following position:\n\n"
                    message_employer += f"Job Title: {job_application.job.title}\n"
                    message_employer += f"Applicant: {request.user.username} (Email: {request.user.email})\n\n"
                    message_employer += "Please take necessary action.\n\nBest regards,\nYour Company Name"
                    send_mail(subject_employer, message_employer, 'your@example.com', [employer_email])

                    return HttpResponse('<script>alert("Job applied successfully."); window.location.replace("/apply_jobs");</script>')
            else:
                form = JobApplicationForm()
            return render(request, 'submit_job.html', {'form': form})
    else:
        return redirect('login')

    
@login_required
def manage_job_applications(request):
    try:
        current_company = request.user.companyprofile
    except CompanyProfile.DoesNotExist:
        return HttpResponse('<script>alert("Please create a company profile first."); window.location.replace("/create_or_edit_company_profile");</script>')

    job_listings = JobListing.objects.filter(company=current_company)
    job_applications = JobApplication.objects.filter(job__in=job_listings)

    return render(request, 'manage_job_applications.html', {'job_applications': job_applications})


@login_required
def view_job_seeker_profile(request, user_id):
    # Retrieve the job seeker's complete profile based on user_id
    job_seeker_profile = get_object_or_404(Profile, user_id=user_id)

    # Filter job applications associated with the job seeker
    job_applications = JobApplication.objects.filter(user_id=user_id, job__company=request.user.companyprofile)

    # Render the profile and job applications in a template
    return render(request, 'job_seeker_profile.html', {'profile': job_seeker_profile, 'job_applications': job_applications})

@login_required
def update_application_status(request, application_id):
    job_application = get_object_or_404(JobApplication, id=application_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        job_application.status = new_status
        job_application.save()
        # Optionally, you can add a success message here
        return HttpResponse('<script>alert("Status updated"); window.location.replace("/manage_job_applications");</script>')

    # If the request is not POST, render the template with the job application
    return render(request, 'update_application_status.html', {'job_application': job_application})

@login_required
def applied_jobs_status(request):
    # Retrieve the job applications associated with the current user
    job_applications = JobApplication.objects.filter(user=request.user)

    return render(request, 'applied_jobs.html', {'job_applications': job_applications})
from django.db.models import Count, Q

@login_required
def view_reports(request):
    # Query to retrieve job reports
    job_reports = JobListing.objects.annotate(
        num_applicants=Count('jobapplication'),
        num_accepted=Count('jobapplication', filter=Q(jobapplication__status='accepted')),
        num_rejected=Count('jobapplication', filter=Q(jobapplication__status='rejected'))
    ).values('company__company_name', 'title', 'num_applicants', 'num_accepted', 'num_rejected')

    return render(request, 'analytics.html', {'job_reports': job_reports})
