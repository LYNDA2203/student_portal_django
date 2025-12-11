from django.shortcuts import render
from .serializer import *
from rest_framework import viewsets
from courses.models import CourseTrack, Course, CourseModule
from mentor.models import Student,Mark,Mentor
from rest_framework.permissions import IsAuthenticated
from .permission import *
from rest_framework.response import Response
from rest_framework.decorators import action

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
    
    @action(detail=True, methods=['get'])
    def marks(self, request, pk=None):
        student = self.get_object()
        marks = Mark.objects.filter(student=student)
        return Response(MarkSerializer(marks, many=True).data)

class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = [IsAuthenticated, MarkPermissions]

    def get_queryset(self):
        # Both student and mentor can see all marks
        return Mark.objects.all()
    
class MentorViewSet(viewsets.ModelViewSet):
    queryset=Mentor.objects.all()
    serializer_class=MentorSerializer
    