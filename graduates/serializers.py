from import_export import fields
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import AcademicHistory, Student, Profile


class StudentSerializer(ModelSerializer):
    inst_name = serializers.ReadOnlyField(source ='institution.name')
    #profiles = serializers.SerializerMethodField()
    class Meta:
        model=Student
        fields = ('id','first_name','middle_name','last_name','inst_name')
        
    
    # def get_profiles(self, obj):
    #     data = ProfileSerializer(obj.profile.all(), many=True).data  
    #     return data  


class ProfileSerializer(ModelSerializer):
    class Meta:
        model=Profile
        fields= ('student', 'image')

  