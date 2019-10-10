from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import CellGroup, Member, Contribution, Payment
from users.models import Role


class MembersUploadForm(forms.Form):
    members_file = forms.FileField()


class AddCellUserForm(forms.Form):
    def __init__(self, company_id=None, *args, **kwargs):
        super(AddCellUserForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField()
        self.fields['email'] = forms.EmailField()
