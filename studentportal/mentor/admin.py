from django.contrib import admin
from .models import Course, Student, Mark

@admin.register(Course)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user',)

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks_obtained', 'max_marks', 'percentage', 'grade')



