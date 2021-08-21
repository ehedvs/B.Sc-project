# Generated by Django 3.2 on 2021-08-20 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0008_alter_university_name'),
        ('registrar_admin', '0006_alter_faculty_total_programs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='total_programs',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='faculty',
            unique_together={('university', 'name')},
        ),
    ]