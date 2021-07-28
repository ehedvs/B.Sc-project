# Generated by Django 3.2 on 2021-07-07 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduates', '0011_auto_20210705_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='academichistory',
            name='uploaded_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='academichistory',
            name='batch',
            field=models.CharField(choices=[('1', 'Freshman'), ('2', 'Sophomore'), ('3', 'Junior'), ('4', 'Senior'), ('5', 'Graduate')], max_length=20),
        ),
    ]