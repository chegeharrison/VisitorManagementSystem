from django.urls import path
from .views import home,loginPage, new_visitor, visitor_detail, visitors_record, log_out_visitor,security_guard_login, security_guard_logout, security_guard_dashboard, department_admin_dashboard, department_admin_login, department_admin_logout,check_in_visitor,check_out_visitor

urlpatterns = [
    path("", home, name='home'),
    path('login/', loginPage, name='login'),
    path('new_visitor/', new_visitor, name='new_visitor'),
    path('visitor_detail/<int:visitor_id>/', visitor_detail, name='visitor_detail'),
    path('visitors_record/', visitors_record, name='visitors_record'),
    path('security_guard_login/', security_guard_login, name='security_guard_login'),
    path('security_guard_logout/', security_guard_logout, name='security_guard_logout'),
    path('security-guard/', security_guard_dashboard, name='security_guard_dashboard'),
    path('department-admin/', department_admin_dashboard, name='department_admin_dashboard'),
    path('department_admin_login/', department_admin_login, name='department_admin_login'),
    path('department_admin_logout/', department_admin_logout, name='department_admin_logout'),
    path('department-admin/check-in-visitor/<int:visitor_id>/', check_in_visitor, name='check_in_visitor'),
    path('department-admin/check-out-visitor/<int:visitor_id>/', check_out_visitor, name='check_out_visitor'),
    
    path('log_out_visitor/<int:visitor_id>', log_out_visitor, name='log_out_visitor')
]