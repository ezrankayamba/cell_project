from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CellGroup, Member, Contribution, Payment
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django import forms
# from .forms import CellGroupForm
from django.urls import reverse
from django.db.models import Avg, Count, Min, Sum
from django.http import HttpResponse
from .resources import MemberResource
from tablib import Dataset
from .forms import MembersUploadForm, AddCellUserForm


def home(request):
    member = None
    try:
        member = request.user.member if request.user.is_authenticated else None
    except Exception as e:
        print(e)
    contr_summary = []
    if member:
        contr_summary = Contribution.objects.filter(cell_group=member.cell_group).annotate(
            p_count=Count('payment'), p_total=Sum('payment__amount'))
    context = {
        'contr_summary': contr_summary
    }
    return render(request, 'cell/home.html', context)


class CreateCellGroupView(LoginRequiredMixin, CreateView):
    model = CellGroup
    fields = ['name']
    template_name = 'cell/cell_group_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CreateMemberView(LoginRequiredMixin, CreateView):
    model = Member
    fields = ['name', 'phone_no']
    template_name = 'cell/cell_member_form.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.cell_group = user.member.cell_group
        return super().form_valid(form)


class CreateContributionView(LoginRequiredMixin, CreateView):
    model = Contribution
    fields = ['name', 'amount']
    template_name = 'cell/cell_contribution_form.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.cell_group = user.member.cell_group
        return super().form_valid(form)


class CreatePaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    fields = ['member', 'contribution', 'amount']
    template_name = 'cell/cell_payment_form.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.cell_group = user.member.cell_group
        return super().form_valid(form)


class MembersUploadView(FormView):
    template_name = 'cell/members_upload.html'
    form_class = MembersUploadForm
    success_url = '/'
    fields = ['members_file']

    def form_valid(self, form):
        mr = MemberResource()
        dataset = Dataset()
        new_members = self.request.FILES['members_file']
        cell_group_id = self.request.user.member.cell_group.id
        user_id = self.request.user.id

        data = dataset.load(new_members.read())

        data.append_col((cell_group_id,) * data.height, header='cell_group')
        data.append_col((user_id,) * data.height, header='created_by')
        result = mr.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            mr.import_data(dataset, dry_run=False)  # Actually import now
        else:
            print('Errors: ', result.row_errors()[0][1][0].error)
        return super().form_valid(form)


class CellUserCreateView(LoginRequiredMixin, FormView):
    form_class = AddCellUserForm
    template_name = 'cell/user_form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        member_id = self.kwargs.get('member_id')
        kwargs['member'] = Member.objects.get(pk=member_id)
        return super(CellUserCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        member_id = self.kwargs.get('member_id')
        data = form.cleaned_data
        user = User(username=data['username'], email=data['email'])
        user.set_password('Cell19')
        user.save()
        member = Member.objects.get(pk=member_id)
        member.user = user
        member.save()
        return super().form_valid(form)


def export_members(request):
    mr = MemberResource()
    dataset = mr.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'
    return response


def members_upload(request):
    if request.method == 'POST':
        mr = MemberResource()
        dataset = Dataset()
        new_members = request.FILES['members_file']

        imported_data = dataset.load(new_members.read())
        result = mr.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            mr.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'cell/members_upload.html')
