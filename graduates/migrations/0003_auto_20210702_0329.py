# Generated by Django 3.2 on 2021-07-02 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('graduates', '0002_auto_20210630_0308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acadamichistory',
            old_name='acadamic_status',
            new_name='academic_status',
        ),
        migrations.AddField(
            model_name='acadamichistory',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
