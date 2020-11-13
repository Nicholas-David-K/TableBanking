# Generated by Django 3.1.2 on 2020-11-13 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tLoans', '0011_auto_20201111_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Helen', max_length=10)),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d/')),
            ],
        ),
    ]
