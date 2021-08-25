from django.db import models
from django.db.models.query import FlatValuesListIterable
from django.shortcuts import redirect
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from super_admin.models import University
from.models import  Student, AcademicHistory
from django.contrib.auth import get_user_model

class StudentResource(resources.ModelResource):
    institution = fields.Field(
        column_name='institution',
        attribute ='institution',
        
        widget = ForeignKeyWidget(University, 'id')
    )
  
    created_by = fields.Field(
        column_name='created_by',
        attribute ='created_by',
        
        widget = ForeignKeyWidget(get_user_model(), 'id')
    )    

    def before_import_row(self, row, row_number, **kwargs):
        row['institution'] = kwargs['institution']
        row['registration_year'] = kwargs['reg_year']
        row['created_by'] = kwargs['created_by']
        
   
    
    class Meta:
        model=Student
        skip_unchanged = False
        report_skipped = True
        fields = ( 'id', 'full_name', 'gender', 'age', 'registration_year')
   

class AcademicalResource(resources.ModelResource):
    student = fields.Field(
        column_name='student',
        attribute ='student',
        
        widget = ForeignKeyWidget(Student, 'id')
    )
    uploaded_by = fields.Field(
        column_name='uploaded_by',
        attribute ='uploaded_by',
        
        widget = ForeignKeyWidget(get_user_model(), 'id')
    ) 
    class Meta:
        model=AcademicHistory
        skip_unchanged = True
        report_skipped = False
        import_id_fields=('student','batch','semester')
        
        fields = ('student', 'batch','semester', 'GPA','CGPA')
    
    def before_import_row(self, row, row_number, **kwargs):
        row['uploaded_by'] = kwargs['uploaded_by']
        row['uploaded_date'] = kwargs['uploaded_date']

    def before_save_instance(self, instance, using_transactions, dry_run):
        if instance.GPA > 4.0:
            raise ValueError("GPA cannot be greater than 4.0")
        elif instance.GPA < 1.5:
            raise ValueError("GPA cannot be less than 1.5")
        elif instance.CGPA > 4.0:
            raise ValueError("CGPA cannot be greater than 4.0")
        elif instance.GPA < 1.5:
            raise ValueError("CGPA cannot be less than 1.5")
        else:
            return super().before_save_instance(instance, using_transactions, dry_run)



