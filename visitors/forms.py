from django import forms
from .models import Visitor, Department

class VisitorForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'First Name'}), required=True, max_length=15)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'Last  Name'}), required=True, max_length=15)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'Email Id'}), required=True, max_length=50)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'Phone'}), required=True, max_length=10)
    id_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 17rem', 'placeholder': 'ID Number'}), required=True, initial=0)
    id_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'style': 'width: 17rem'}), required=False)
    attended = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 17rem'}), required=False)

    class Meta:
        model = Visitor
        fields = ['first_name', 'last_name', 'id_number', 'id_image', 'phone', 'department']


class SecurityGuardLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
