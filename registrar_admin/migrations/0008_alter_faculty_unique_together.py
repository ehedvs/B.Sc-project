# Generated by Django 3.2 on 2021-08-20 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar_admin', '0007_auto_20210820_1313'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='faculty',
            unique_together=set(),
        ),
    ]