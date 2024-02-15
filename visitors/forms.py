from django import forms
from .models import Visitor, Department

class VisitorForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'First Name'}), required=True, max_length=15)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'Last  Name'}), required=True, max_length=15)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'Email Id'}), required=True, max_length=50)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'Phone'}), required=True, max_length=10)
    id_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'ID Number'}), required=True)
    id_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'style': 'width: 17rem','placeholder':'ID Image'}), required=False)
    attended = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder':'Choose Visiting Department'}), required=False)


    
    class Meta:
        model = Visitor
        fields = ['first_name', 'last_name', 'id_number', 'id_image', 'phone', 'department']


class SecurityGuardLoginForm(forms.Form):
    username = forms.CharField( max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput,label='Password')

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label=None, label='Department')

