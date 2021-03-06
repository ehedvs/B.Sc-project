# Generated by Django 3.2 on 2021-08-25 21:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0011_auto_20210825_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='fax_no',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be in format of  +251930598989', regex='^(\\+251)\\d{9}$')]),
        ),
        migrations.AlterField(
            model_name='university',
            name='phone_no1',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be in format of  +251930598989', regex='^(\\+251)\\d{9}$')]),
        ),
    ]
