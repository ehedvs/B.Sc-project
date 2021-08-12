from django.db import models
from django.db.models.query import FlatValuesListIterable
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from super_admin.models import University
from.models import Certificate, Student, AcademicHistory
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
        fields = ( 'id', 'first_name','middle_name', 'last_name', 'gender', 'age', 'registration_year')
   

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
        
        fields = ('student', 'batch','semester', 'academic_status')
    
    def before_import_row(self, row, row_number, **kwargs):
        row['uploaded_by'] = kwargs['uploaded_by']
        row['uploaded_date'] = kwargs['uploaded_date']


class CertificateResource(resources.ModelResource):
    student = fields.Field(
        column_name='student',
        attribute ='student',
        
        widget = ForeignKeyWidget(Student, 'id')
    )
    class Meta:
        model=Certificate
        skip_unchanged = True
        report_skipped = False
        import_id_fields=('student',)
        fields = ('student', 'school','dept', 'GPA','CGPA')

        def before_import_row(self, row, row_number, **kwargs):
            row['uploaded_date'] = kwargs['uploaded_date']
            
        