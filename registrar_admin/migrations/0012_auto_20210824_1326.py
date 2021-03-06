# Generated by Django 3.2 on 2021-08-24 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registrar_admin', '0011_alter_faculty_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='reciever',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='super_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='request',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrar_admin', to=settings.AUTH_USER_MODEL),
        ),
    ]
