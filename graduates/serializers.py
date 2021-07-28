from import_export import fields
from rest_framework.serializers import ModelSerializer
from .models import Student, Profile


class StudentSerializer(ModelSerializer):
    class Meta:
        model=Student
        fields = '__all__'


class ProfileSerializer(ModelSerializer):
    class Meta:
        model=Profile
        fields= '__all__'
  