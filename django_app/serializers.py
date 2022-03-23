from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'        

class DepartmentSerializer(serializers.ModelSerializer):
    # university = UniversitySerializer()

    class Meta:
      model = Department
      fields='__all__'   

class SpecializationSerializer(serializers.ModelSerializer):
    # university = UniversitySerializer()

    class Meta:
      model = Specialization
      fields='__all__' 

class SemesterSerializer(serializers.ModelSerializer):
    # university = UniversitySerializer()

    class Meta:
      model = Semester
      fields='__all__' 

class SubjectSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()

    class Meta:
      model = Subject
      fields='__all__' 

class ModuleSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()

    class Meta:
      model = Module
      fields='__all__' 

class TeacherSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()

    class Meta:
      model = Teacher
      fields='__all__' 

class VideoSerializer(serializers.ModelSerializer):
    # university = UniversitySerializer()

    class Meta:
      model = Video
      fields='__all__' 

class CourseSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()
    department = DepartmentSerializer()
    specialization = SpecializationSerializer()
    semester = SemesterSerializer()
    video = VideoSerializer()
    # subject = SubjectSerializer()
    # module = ModuleSerializer()

    class Meta:
        model = Course
        fields = '__all__'        
      
class PurchasedCourseSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()
    department = DepartmentSerializer()
    specialization = SpecializationSerializer()
    semester = SemesterSerializer()
    
    class Meta:
        model = PurchasedCourse
        fields = '__all__'        

class StarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarRating
        fields='__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields='__all__'              
