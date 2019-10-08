from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import CellGroup, CellUser, Member, Contribution, Payment
from users.models import Role


class MembersUploadForm(forms.Form):
    members_file = forms.FileField()
