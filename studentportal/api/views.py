from django.shortcuts import render
from .serializer import CourseTrackSerializer,CourseSerializer, CourseModuleSerializer,StudentSerializer,MarkSerializer,MentorSerializer
from rest_framework import viewsets
from courses.models import CourseTrack, Course, CourseModule
from mentor.models import Student,Mark,Mentor

# Create your views here.
class CourseTrackViewSet(viewsets.ModelViewSet):
    queryset=CourseTrack.objects.all()
    serializer_class=CourseTrackSerializer
    
class CourseViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class=CourseSerializer
    
class CourseModuleViewSet(viewsets.ModelViewSet):
    queryset=CourseModule.objects.all()
    serializer_class=CourseModuleSerializer
    
class StudentViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

class MarkViewSet(viewsets.ModelViewSet):
    queryset=Mark.objects.all()
    serializer_class=MarkSerializer
    
class MentorViewSet(viewsets.ModelViewSet):
    queryset=Mentor.objects.all()
    serializer_class=MentorSerializer
    