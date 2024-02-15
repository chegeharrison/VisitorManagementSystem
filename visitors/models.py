from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    name =models.CharField(max_length=50)

    def __str__(self): 
        return self.name
    
class DepartmentAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[('security', 'Security Guard'), ('department', 'Department Admin')], default='security')
    department = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default=1)
  
    def __str__(self):
        return self.user.username

    


class Visitor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10)
    id_number = models.IntegerField(default=0)
    id_image = models.ImageField(upload_to='static/media', null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now())
    time_in = models.TimeField(default=datetime.datetime.now())
    time_out = models.TimeField(null=True, blank=True)
    attended = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    department_admin = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - ID {self.id}"
    



class SecurityGuard(models.Model):
    id = models.AutoField
    staff_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    time_sign_in = models.DateTimeField(null=True, blank=True)
    time_sign_out = models.DateTimeField(null=True, blank=True)
    GATE_CHOICES = [
        ('Gate A', 'Gate A'),
        ('Gate B', 'Gate B'),
        ('Gate C', 'Gate C'),
    ]
    working_gate = models.CharField(max_length=10, choices=GATE_CHOICES)

    def __str__(self):
        return str(self.id) + " : " + str(self.name)