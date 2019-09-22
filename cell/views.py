from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CellGroup, CellUser, Member, Contribution, Payment
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django import forms
# from .forms import CellGroupForm
from django.urls import reverse
from django.db.models import Avg, Count, Min, Sum


def home(request):
    cell_user = request.user.celluser
    contr_summary = []
    if cell_user:
        contr_summary = Contribution.objects.filter(cell_group=request.user.celluser.cell_group).annotate(
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
    fields = ['name']
    template_name = 'cell/cell_member_form.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.cell_group = user.celluser.cell_group
        return super().form_valid(form)


class CreateContributionView(LoginRequiredMixin, CreateView):
    model = Contribution
    fields = ['name', 'amount']
    template_name = 'cell/cell_contribution_form.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.cell_group = user.celluser.cell_group
        return super().form_valid(form)


class CreatePaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    fields = ['member', 'contribution', 'amount']
    template_name = 'cell/cell_payment_form.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.cell_group = user.celluser.cell_group
        return super().form_valid(form)
