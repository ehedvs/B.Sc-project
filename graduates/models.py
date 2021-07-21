from typing import Tuple
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from super_admin.models import University
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from accounts.models import User
from django.contrib.auth import get_user_model

#from ehedvs import settings




class Student(models.Model):
    institution = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
    id = models.CharField(max_length=200, primary_key=True, verbose_name='ID Number ')
    first_name = models.CharField(max_length=200, verbose_name='first name')
    middle_name = models.CharField(max_length=200, verbose_name='middle name')
    last_name =  models.CharField(max_length=200, verbose_name='last name')
    gender = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    registration_year = models.DateField(auto_now_add=True, null=True, verbose_name='Registration_Date')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + " " + self.middle_name + " "+self.last_name

    
   

    

class AcademicHistory(models.Model):
     sem = (
        ('1', '1st semester'),
        ('2', '2nd semester'),
    )
     status = (
        ('promoted', 'promoted'),
        ('failed', 'failed'),
        ('suspended', 'suspended')
    )
     batch = (
        ('1', 'Freshman'),
        ('2', 'Sophomore'),
        ('3', 'Junior'),
        ('4', 'Senior'),
        ('5', 'Graduate'),
    )
    
     student = models.ForeignKey(Student,  on_delete=models.CASCADE)
     batch = models.CharField(max_length=20, choices=batch)
     semester = models.CharField(max_length=20, choices=sem)
     academic_status= models.CharField(max_length=20, choices=status)
     uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
     uploaded_date = models.DateTimeField(auto_now=True)

     
     def __str__(self):
        return f'{self.student  } Academical status'
        



    
   


class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to ='qr_codes')
    image = models.ImageField(default ='default.png', upload_to='student_image' )

    def __str__(self):
        return f'{self.student.first_name} Profile'
   



    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.student.id)
        canvas = Image.new('RGB', (320, 320), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.student.id}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
        


class Certificate(models.Model):
    student = models.ForeignKey(Student,  on_delete=models.CASCADE, verbose_name='student_id')
    school= models.CharField(max_length=200, )
    dept = models.CharField(max_length=200,  verbose_name='Department')
    GPA = models.FloatField(default=0.0 )
    CGPA = models.FloatField(default=0.0 )


    def __str__(self):
        return f'{self.student } Certificate'









