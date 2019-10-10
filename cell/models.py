from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from auditlog.registry import auditlog
from auditlog.models import LogEntry


class CellGroup(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    record_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('home')


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    cell_group = models.ForeignKey(CellGroup, on_delete=models.CASCADE)
    record_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='member_created_by')
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=20, null=True)

    class Meta:
        unique_together = ('name', 'cell_group',)
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('create-member')


class Contribution(models.Model):
    cell_group = models.ForeignKey(CellGroup, on_delete=models.CASCADE)
    record_date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='contribution_created_by')

    class Meta:
        ordering = ['-record_date']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('create-contribution')


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    record_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='payment_created_by')
    cell_group = models.ForeignKey(CellGroup, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-record_date']

    def __str__(self):
        return f'{self.member} - {self.contribution} - {self.amount}'

    def get_absolute_url(self):
        return reverse('create-payment')


# Audit Logs
auditlog.register(CellGroup)
auditlog.register(Member)
auditlog.register(Contribution)
auditlog.register(Payment)
