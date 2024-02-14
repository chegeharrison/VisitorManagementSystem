from django.contrib import admin
from . models import Visitor
from .models import Department

# Register your models here.
admin.site.register(Visitor)
admin.site.register(Department)