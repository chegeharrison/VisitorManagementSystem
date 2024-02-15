from django.contrib import admin
from . models import Visitor
from .models import Department
from .models import  UserProfile
from .models import SecurityGuard
from .models import DepartmentAdmin

# Register your models here.
admin.site.register(Department)
admin.site.register(DepartmentAdmin)
admin.site.register(UserProfile)
admin.site.register(SecurityGuard)
admin.site.register(Visitor)