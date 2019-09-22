from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import CellGroup, CellUser, Member, Contribution, Payment
from users.models import Role


# class CellGroupForm(forms.ModelForm):
#     class Meta:
#         model = CellGroup
#         fields = ['name', 'created_by']
#         widgets = {
#             'created_by': forms.HiddenInput,
#         }
