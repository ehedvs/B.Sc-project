# Generated by Django 3.2 on 2021-06-30 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduates', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acadamichistory',
            name='cgpa',
        ),
        migrations.RemoveField(
            model_name='acadamichistory',
            name='gpa',
        ),
        migrations.AlterField(
            model_name='acadamichistory',
            name='batch',
            field=models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate')], max_length=20),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='qr_code',
            field=models.ImageField(null=True, upload_to='qr_codes'),
        ),
    ]
