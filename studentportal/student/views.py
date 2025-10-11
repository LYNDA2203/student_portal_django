from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mentor.models import Student,UserProfile

@login_required
def student_dashboard(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect("home")
    
    if profile.role != "student":
        return redirect("home")  
    
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect("home")
    
    marks = student.marks.select_related("course")

    return render(request, "student/dashboard.html", {
        "student": student,
        "marks": marks,
    })
