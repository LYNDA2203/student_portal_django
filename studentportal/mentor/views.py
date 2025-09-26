# mentor/views.py

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Student, Mark
from django.contrib.auth.decorators import login_required
from courses.models import Course

@login_required
def student_marks_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    marks = Mark.objects.filter(student=student).select_related("course")

    total_obtained = sum(m.marks_obtained for m in marks)
    total_max = sum(m.max_marks for m in marks)
    overall_percentage = (total_obtained / total_max * 100) if total_max > 0 else 0

    # calculate grade from percentage
    def get_grade(percentage):
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"

    overall_grade = get_grade(overall_percentage)

    context = {
        "student": student,
        "marks": marks,                  
        "total_obtained": total_obtained,
        "total_max": total_max,
        "overall_percentage": overall_percentage,
        "overall_grade": overall_grade,  
    }
    return render(request, "mentor/student_marks.html", context)
@login_required
def student_course_marks_view(request, student_id, course_id):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    mark = Mark.objects.filter(student=student, course=course).first()

    context = {
        'student': student,
        'course': course,
        'mark': mark,
    }
    return render(request, 'mentor/student_course_marks.html', context)