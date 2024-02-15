from django.urls import path
from .views import home, adminLogin, adminLogout, department_admin_dashboard, check_in_visitor,check_out_visitor,    new_visitor, visitor_detail, visitors_record, log_out_visitor,security_guard_login, security_guard_logout, security_guard_dashboard, logout_view

urlpatterns = [
    path("", home, name='home'),
    # admin only
    path('adminlogin/', adminLogin, name='adminLogin'),
    path('adminlogout/', adminLogout, name='adminlogout'),
    path('department-admin/', department_admin_dashboard, name='department_admin_dashboard'),
    path('department-admin/check-in-visitor/<int:visitor_id>/', check_in_visitor, name='check_in_visitor'),
    path('department-admin/check-out-visitor/<int:visitor_id>/', check_out_visitor, name='check_out_visitor'),
    
    # security only
    path('security_guard_login/', security_guard_login, name='security_guard_login'),
    path('security_guard_logout/', security_guard_logout, name='security_guard_logout'),
    path('security-guard/', security_guard_dashboard, name='security_guard_dashboard'),
    path('new_visitor/', new_visitor, name='new_visitor'),
    path('visitors_record/', visitors_record, name='visitors_record'),
    path('visitor_detail/<int:visitor_id>/', visitor_detail, name='visitor_detail'),

    path('logout/', logout_view, name='logout'),
   
   
   
    
    
   
    
    
    
    path('log_out_visitor/<int:visitor_id>', log_out_visitor, name='log_out_visitor')
]