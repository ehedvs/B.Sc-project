from django.forms import ModelForm, fields
from django import forms
from .models import AcademicHistory, Profile, Student

class AcademicHistoryForm(ModelForm):
    class Meta:
        model=AcademicHistory
        fields='__all__'



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class DateInput(forms.DateInput):
    input_type= 'date'
    

class ExapleForm(forms.Form):
    Select_date = forms.DateField( widget=DateInput)
    