from django import forms
from .models import *


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=50)
    # password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['role']
        labels = {'role': 'Роль'}


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = '__all__'


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = "__all__"
        widgets = {
            'price_unit': forms.NumberInput(attrs = {'min': 0.00, 'step': '0.01', 'placeholder': '0.00'}),
            'min_qty': forms.NumberInput(attrs = {'min': 0, 'step': '1', 'placeholder': '0'}),
        }