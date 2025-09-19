# mentor/views.py

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Student, Mark,Course
from django.contrib.auth.decorators import login_required

@login_required
def student_marks_view(request, student_id):
    try:
        student = request.user.student  # assuming OneToOne relation from Student to User
    except Student.DoesNotExist:
        raise Http404("No Student profile for current user")
    marks = student.marks.select_related('course').all()  # use select_related to avoid many queries
    total_obtained = sum(m.marks_obtained for m in marks)
    total_max = sum(m.max_marks for m in marks)
    overall_percentage = (total_obtained / total_max * 100) if total_max else 0
    # compute overall_grade similar to before

    context = {
        'student': student,
        'marks': marks,
        'total_obtained': total_obtained,
        'total_max': total_max,
        'overall_percentage': overall_percentage,
        # 'overall_grade': overall_grade,
    }
    return render(request, 'mentor/student_marks.html', context)

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
    return render(request, 'mentor/student_course_mark.html', context)