from django.forms import ModelForm
from .models import Faculty, Program
class FacultyForms(ModelForm):
    class Meta:
        model=Faculty
        fields='__all__'
        labels = {
        'name':'Name of faculty',
        
        }

class ProgramForms(ModelForm):
    class Meta:
        model=Program
        fields='__all__'
        labels = {
        'name':'Name of program',
        
        }
    def __init__(self, logged_univ, *args, **kwargs):
        super(ProgramForms, self).__init__(*args,**kwargs)
        self.fields['faculty'].queryset=Faculty.objects.filter(university=logged_univ)

