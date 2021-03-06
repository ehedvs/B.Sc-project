# Generated by Django 3.2 on 2021-07-15 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduates', '0012_auto_20210707_0312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='qr_code',
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='student',
        ),
        migrations.AddField(
            model_name='student',
            name='qr_code',
            field=models.ImageField(null=True, upload_to='qr_codes'),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=200, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='ID Number'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=200, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(max_length=200, verbose_name='middle name'),
        ),
    ]
