# Generated by Django 3.2 on 2021-07-19 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduates', '0022_student_registration_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_year',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Registration_Date'),
        ),
    ]