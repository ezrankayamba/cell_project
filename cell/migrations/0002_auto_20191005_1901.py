# Generated by Django 2.2.5 on 2019-10-05 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cell', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('name', 'cell_group')},
        ),
    ]