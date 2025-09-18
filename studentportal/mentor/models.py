from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='mentor_student')
    full_name = models.CharField(max_length=200)
    # additional fields: roll_no, etc.

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.full_name

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks_obtained = models.PositiveIntegerField()
    max_marks = models.PositiveIntegerField(default=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='student_course_marks')
        ]
        verbose_name = "Mark"
        verbose_name_plural = "Marks"
    
    def clean(self):
        if self.marks_obtained > self.max_marks:
            raise ValidationError("Marks obtained cannot exceed max marks.")

    @property
    def percentage(self):
        if self.max_marks == 0:
            return 0
        return (self.marks_obtained / self.max_marks) * 100

    @property
    def grade(self):
        p = self.percentage
        if p >= 90:
            return 'A'
        elif p >= 80:
            return 'B'
        elif p >= 70:
            return 'C'
        elif p >= 60:
            return 'D'
        else:
            return 'F'

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name} : {self.marks_obtained}/{self.max_marks}"

