from rest_framework import serializers
from courses.models import CourseTrack, Course, CourseModule
from mentor.models import Student,Mark,Mentor

class CourseTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseTrack
        fields="__all__"
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields="__all__"
        
class CourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseModule
        fields="__all__"
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"
        
class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mark
        fields="__all__"
        
class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentor
        fields="__all__"
        
        