from django.db import models
from super_admin.models import University



class Faculty(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    total_programs = models.IntegerField()

    def __str__(self):
        return self.name


class Program(models.Model):
    degree_type =(
        (
           'BA','Bachelor of  Art',
        ),
        (
            'BSc','Bachelor of Science'
        ),
        (
           'BEd','Bachelor of Science'
        ),
        (
            'MD','Master of Doctorate'
        ),
        (
            'BPH', 'Bachelor of Pharmacy'
        ),

    )
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    year_required = models.IntegerField()
    degree_type = models.CharField(max_length=50, choices=degree_type)

    def __str__(self):
        return self.name


