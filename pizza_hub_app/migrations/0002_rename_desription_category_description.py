# Generated by Django 5.1.7 on 2025-04-08 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_hub_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='desription',
            new_name='description',
        ),
    ]
