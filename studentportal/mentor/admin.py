from django.contrib import admin
from .models import Course, Student, Mark,UserProfile,Mentor

@admin.register(Course)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mentor_username')
    
    def mentor_username(self, obj):
        if obj.mentor:
            return obj.mentor.full_name or obj.mentor.user.username
        return '-'
    
    mentor_username.short_description = 'Mentor Name'

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks_obtained', 'max_marks', 'percentage', 'grade')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
