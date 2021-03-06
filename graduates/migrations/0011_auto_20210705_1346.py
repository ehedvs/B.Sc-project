# Generated by Django 3.2 on 2021-07-05 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('graduates', '0010_auto_20210705_0430'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate')], max_length=20)),
                ('semester', models.CharField(choices=[('1', '1st semester'), ('2', '2nd semester')], max_length=20)),
                ('academic_status', models.CharField(choices=[('promoted', 'promoted'), ('failed', 'failed'), ('suspended', 'suspended')], max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='stud_id',
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='student_id'),
        ),
        migrations.DeleteModel(
            name='AcadamicHistory',
        ),
        migrations.AddField(
            model_name='academichistory',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graduates.student'),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
