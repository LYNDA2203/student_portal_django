from django.contrib import admin
from .models import Course, Student, Mark,UserProfile

@admin.register(Course)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mentor_username')
    
    def mentor_username(self, obj):
        return obj.user.username
    mentor_username.short_description = 'Mentor Name'

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks_obtained', 'max_marks', 'percentage', 'grade')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
