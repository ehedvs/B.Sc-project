from import_export import fields
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import AcademicHistory, Student, Profile, Certificate

class CertificateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source = 'student.first_name')
    middle_name = serializers.CharField(source = 'student.middle_name')
    last_name = serializers.CharField(source = 'student.last_name')
    institution  = serializers.CharField(source = 'student.institution')
    class Meta:
        model = Certificate
        fields = ['student', 'first_name', 'middle_name','last_name', 'institution', 'school', 'dept','GPA','CGPA']

class StudentSerializer(ModelSerializer):
    institution = serializers.ReadOnlyField(source ='institution.name')
    #profiles = serializers.SerializerMethodField()
    class Meta:
        model=Student
        fields = ('id','first_name','middle_name','last_name','institution')
        
        
    
    # def get_profiles(self, obj):
    #     data = ProfileSerializer(obj.profile.all(), many=True).data  
    #     return data  


class ProfileSerializer( serializers.ModelSerializer):

    class Meta:
        model=Profile
        fields =['student', 'image',]
        


  