# Generated by Django 3.2 on 2021-08-20 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar_admin', '0005_alter_faculty_total_programs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='total_programs',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
