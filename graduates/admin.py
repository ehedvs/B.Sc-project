from django.contrib import admin
from .models import Student, AcademicHistory, Certificate,Profile

admin.site.register(Student)
admin.site.register(Certificate)
admin.site.register(AcademicHistory)
admin.site.register(Profile)


