# Generated by Django 3.1.2 on 2020-11-08 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tLoans', '0004_auto_20201108_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='long_term',
            name='long_term_interest_repayment',
        ),
    ]
