from rest_framework import serializers
from courses.models import CourseTrack, Course, CourseModule
from mentor.models import Student,Mark,Mentor

class CourseTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseTrack
        fields="__all__"
        
class CourseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_name(self, obj):
        return obj.track.title

class CourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseModule
        fields="__all__"
        

class MarkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Mark
        fields = [ "id", "student", "student_name", "course", "course_name", "marks_obtained","max_marks"]
    def get_course_name(self, obj):
        return obj.course.track.title    # return the track title directly

class StudentSerializer(serializers.ModelSerializer):
    mentor_name = serializers.CharField(source="mentor.full_name", read_only=True)
    # nested marks
    marks = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "mentor_name", "marks"]  # includes 'marks' and 'mentor_name'

    def get_marks(self, obj):
        qs = obj.marks.all()  # related_name='marks' on Mark.student
        return MarkSerializer(qs, many=True).data

    def validate_full_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must contain at least 3 characters")
        return value

        
class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentor
        fields="__all__"
        
        