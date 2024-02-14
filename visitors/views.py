from django.shortcuts import render, redirect, get_object_or_404
from .forms import VisitorForm,SecurityGuardLoginForm
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

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")  # Assuming you have a 'home' named URL pattern
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'visitors/new_visitors')

    else:
        return render(request, 'register/admin_login.html')

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


@login_required(login_url='/admin_login/')
def new_visitor(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST, request.FILES)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.time_in = timezone.now()
            visitor.save()
            return redirect('security/security_guard_dashboard')
    else:
        form = VisitorForm()

    return render(request, 'visitor/new_visitor.html', {'form': form})

    
def visitor_detail(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)
    return render(request, 'visitor/visitor_detail.html', {'visitor': visitor})

def visitors_record(request):
    # Get all visitors for the current day and order them by time_in
    today = timezone.now().date()
    visitors = Visitor.objects.filter(date__date=today).order_by('time_in')
    
    return render(request, 'visitor/visitors_record.html', {'visitors': visitors})


def log_out_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)

      # Check if the current user is a Department Admin

    if request.user.is_authenticated and request.user.is_department_admin:
        visitor.exit_time = timezone.now()
        visitor.attended = True  # Set attended to "Yes"
        visitor.save()
    
    return redirect('success_page')  # Redirect to a success page


def department_admin_dashboard(request):
    # Assuming the department is chosen based on the logged-in user or some other logic
    department = request.user.department
    visitors = Visitor.objects.filter(department=department).order_by('time_in')
    return render(request, 'department_admin_dashboard.html', {'visitors': visitors})

def check_in_visitor(request, visitor_id):
    visitor = Visitor.objects.get(pk=visitor_id)
    visitor.attended = True
    visitor.save()
    return redirect('department_admin_dashboard')



# In the security guard views
def check_out_visitor(request, visitor_id):
    visitor = Visitor.objects.get(pk=visitor_id)
    visitor.check_out_time = datetime.datetime.now().time()
    visitor.save()
    return redirect('security/security_guard_dashboard')
# In the department admin views
def check_out_visitor(request, visitor_id):
    visitor = Visitor.objects.get(pk=visitor_id)
    visitor.check_out_time = datetime.datetime.now().time()
    visitor.save()
    return redirect('security/department_admin_dashboard')

def security_guard_login(request):
    if request.method == 'POST':
        form = SecurityGuardLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('new_visitor')  # Redirect to the desired view after successful login
            else:
                # Invalid credentials, handle accordingly
                messages.error(request, 'Invalid username or password.')
                pass
    else:
        form = SecurityGuardLoginForm()

    return render(request, 'register/security_guard_login.html', {'form': form})
def security_guard_logout(request):
    logout(request)
    return redirect('home')

def department_admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user and user.userprofile.user_type == 'department':
            login(request, user)
            return redirect('department_admin_dashboard')
        else:
            messages.error(request, 'Invalid login credentials or user type.')
            return redirect('department_admin_login')

    return render(request, 'your_department_admin_login_template.html')

@login_required
def department_admin_logout(request):
    logout(request)
    return redirect('home')
