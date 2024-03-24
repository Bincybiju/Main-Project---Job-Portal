from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.views.generic import FormView


def index(request):
    return render(request,'index.html')

def employer(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'employer'
            user.is_staff=True
            user.save()
            login(request, user)  
            request.session['registration_success'] = True
            return HttpResponse('<script>alert("Registration successful! Please login to continue."); window.location.replace("/index");</script>')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'employer_registration.html', {'form': form})

def job_seeker(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'job_seeker'
            user.save()
            login(request, user)  
            request.session['registration_success'] = True
            return HttpResponse('<script>alert("Registration successful! Please login to continue."); window.location.replace("/index");</script>')
    else:
        form = JobSeekerRegistrationForm()
    return render(request, 'jobseeker_registration.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_profile')
            elif user.user_type == 'employer':
                request.session['user_type'] = 'employer'
                return redirect('employer_profile')
            elif user.user_type == 'job_seeker':
                request.session['user_type'] = 'job_seeker'
                return redirect('jobseeker_profile')
        else:
            # Non-registered user alert message
            return HttpResponse('<script>alert(" Invalid credentials. Please try again."); window.location.replace("/login_view");</script>')

    # If it's a GET request, just render the login page
    return render(request, 'login.html')

@login_required
def employer_profile(request):
    if request.session.get('user_type') == 'employer':
        username = request.user.username  # Get the username from the request's user object
        return render(request, 'employer_profile.html', {'username': username})
    else:
        return HttpResponse("Unauthorized", status=401)

@login_required
def jobseeker_profile(request):
    if request.session.get('user_type') == 'job_seeker':
        username = request.user.username  # Get the username from the request's user object
        return render(request, 'jobseeker_profile.html', {'username': username})
    else:
        return HttpResponse("Unauthorized", status=401)
    
@login_required
def admin_profile(request):
    if request.user.is_superuser:
        return render(request, 'admin_profile.html')
    else:
        return HttpResponse("Unauthorized", status=401)

