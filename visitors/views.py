from django.shortcuts import render, redirect, get_object_or_404
from .forms import VisitorForm,SecurityGuardLoginForm,AdminLoginForm
from django.contrib.auth import authenticate, login,logout
from .models import Visitor
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time
today = datetime.now().date()
tomorrow = today + timedelta(1)
today_start = datetime.combine(today, time())
today_end = datetime.combine(tomorrow, time())



# Create your views here.
def home(request):
    return render(request, 'index.html')

# Department Admin
# views.py in your department app

def adminLogin(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        print("Form is valid:", form.is_valid())
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            department = form.cleaned_data['department']

            user = authenticate(request, username=username, password=password)
            print("User:", user)
            print("User profile:", user.userprofile if user else None)

            if user:
                print("User type:", user.userprofile.user_type)
                print("User department:", user.userprofile.department)

                if user.userprofile.user_type == 'department' and user.userprofile.department == department:
                    # Set the user type for department admins
                    user.userprofile.user_type = 'department'
                    user.userprofile.save()

                    login(request, user)
                    return redirect('department_admin_dashboard')
                else:
                    messages.error(request, 'Invalid login credentials or user type.')
            else:
                messages.error(request, 'Authentication failed.')

            return redirect('adminLogin')

    else:
        form = AdminLoginForm()

    return render(request, 'department/admin_login.html', {'form': form})




def adminLogout(request):
    logout(request)
    return redirect('home')




@login_required(login_url='/adminLogin/')

def department_admin_dashboard(request):
    if request.user.is_authenticated and request.user.userprofile.user_type == 'department':
        department_admin = request.user.userprofile
        visitors_queued = Visitor.objects.filter(department_admin=department_admin, time_in__isnull=True)
        visitors_checked_in = Visitor.objects.filter(department_admin=department_admin, time_in__isnull=False, time_out__isnull=True)

        return render(request, 'department/department_admin_dashboard.html', {'department_admin': department_admin, 'visitors_queued': visitors_queued, 'visitors_checked_in': visitors_checked_in})
    else:
        messages.error(request, 'Access Denied')
        return redirect('adminLogin')

def check_in_visitor(request, visitor_id):
    if request.user.is_authenticated and request.user.userprofile.user_type == 'department':
        department_admin = request.user.userprofile
        visitor = get_object_or_404(Visitor, id=visitor_id, department_admin=department_admin, time_in__isnull=True)

        # Perform check-in logic here
        visitor.time_in = timezone.now()
        visitor.save()

        return render(request, 'check_in_success.html', {'visitor': visitor})
    else:
        messages.error(request, 'Access Denied')
        return redirect('department_admin_login')

def check_out_visitor(request, visitor_id):
    if request.user.is_authenticated and request.user.userprofile.user_type == 'department':
        department_admin = request.user.userprofile
        visitor = get_object_or_404(Visitor, id=visitor_id, department_admin=department_admin, time_in__isnull=False, time_out__isnull=True)

        # Perform check-out logic here
        visitor.time_out = timezone.now()
        visitor.save()

        return render(request, 'check_out_success.html', {'visitor': visitor})
    else:
        messages.error(request, 'Access Denied')
        return redirect('department_admin_login')






# Security
# views.py (security guard login view)
def security_guard_login(request):
    if request.method == 'POST':
        form = SecurityGuardLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if the user type is 'security' before logging in
                if user.userprofile.user_type == 'security':
                    login(request, user)
                    return redirect('new_visitor')  # Redirect to the desired view after successful login
                else:
                    # User with 'department' user type trying to access security login
                    messages.error(request, 'Invalid user type for security login.')
            else:
                # Invalid credentials, handle accordingly
                messages.error(request, 'Invalid username or password.')
    else:
        form = SecurityGuardLoginForm()

    return render(request, 'security/security_guard_login.html', {'form': form})
    
def security_guard_logout(request):
    logout(request)
    return redirect('security/security_guard_logout.html')



    

@login_required(login_url='/security_guard_login/')

def security_guard_dashboard(request):
    if request.method == 'POST':
        visitor_id = request.POST.get('visitor_id')
        action = request.POST.get('action')  # 'check_in' or 'check_out'
        
        visitor = Visitor.objects.get(pk=visitor_id)

        if action == 'check_in':
            visitor.attended = True
            visitor.time_in = datetime.datetime.now().time()
        elif action == 'check_out':
            visitor.time_out = datetime.datetime.now().time()

        visitor.save()

    visitors = Visitor.objects.filter(date__date=today).order_by('time_in')
    return render(request, 'security/security_guard_dashboard.html', {'visitors': visitors})


@login_required(login_url='/security_guard_login/')
def new_visitor(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST, request.FILES)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.time_in = timezone.now()
            visitor.save()
            return redirect('security_guard_dashboard')
    else:
        form = VisitorForm()

    return render(request, 'visitor/new_visitor.html', {'form': form})


def check_out_visitor(request, visitor_id):
    visitor = Visitor.objects.get(pk=visitor_id)
    visitor.check_out_time = datetime.datetime.now().time()
    visitor.save()
    return redirect('security/security_guard_dashboard')

def visitors_record(request):
    # Get all visitors for the current day and order them by time_in
    today = timezone.now().date()
    visitors = Visitor.objects.filter(date__date=today).order_by('time_in')
    
    return render(request, 'visitor/visitors_record.html', {'visitors': visitors}) 

  
def visitor_detail(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)
    return render(request, 'visitor/visitor_detail.html', {'visitor': visitor})

def logout_view(request):
    logout(request)
    return redirect('home')





# I cant figure it ou ########################################################################
def log_out_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)

      # Check if the current user is a Department Admin

    if request.user.is_authenticated and request.user.is_department_admin:
        visitor.exit_time = timezone.now()
        visitor.attended = True  # Set attended to "Yes"
        visitor.save()
    
    return redirect('success_page')  # Redirect to a success page








# In the security guard views

# In the department admin views









