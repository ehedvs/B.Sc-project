# Generated by Django 3.2 on 2021-08-12 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduates', '0023_alter_student_registration_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='uploaded_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
