from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CellUser, CellGroup


@receiver(post_save, sender=CellGroup)
def create_cell_user(sender, instance, created, **kwargs):
    if created:
        CellUser.objects.create(
            user=instance.created_by, created_by=instance.created_by, cell_group=instance)
