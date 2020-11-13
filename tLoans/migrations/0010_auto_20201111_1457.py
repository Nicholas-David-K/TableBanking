# Generated by Django 3.1.2 on 2020-11-11 11:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tLoans', '0009_auto_20201111_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='booster',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booster',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
