# Generated by Django 3.2 on 2021-08-25 21:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0010_auto_20210825_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='fax_no',
            field=models.CharField(blank=True, default=1, max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number must be in format of  +251930598989', regex='^(\\+251)\\d{9}$')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='university',
            name='phone_no1',
            field=models.CharField(blank=True, default=1, max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number must be in format of  +251930598989', regex='^(\\+251)\\d{9}$')]),
            preserve_default=False,
        ),
    ]
