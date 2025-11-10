from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from mentor.models import Student,UserProfile,Mark

@login_required
def student_dashboard(request):
    # Ensure the logged-in user has a profile and is a student
    profile = getattr(request.user, "userprofile", None)
    if not profile or profile.role != "student":
        return redirect("home")

    # Get the student object or 404 if missing
    student = get_object_or_404(Student, user=request.user)

    # Get all marks with related course info
    marks = Mark.objects.filter(student=student).select_related("course")

    # Render student dashboard
    return render(request,"student/student_dashboard.html",{"student": student, "marks": marks})