from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from mentor.models import Student,UserProfile,Mark,Mentor
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def student_dashboard(request):
    user = request.user
    
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        return redirect("home")

    if profile.role != "student":
        return redirect("home")

    # Check if student exists
    student, created = Student.objects.get_or_create(
        user=user,
        defaults={'full_name': user.get_full_name() or user.username}
    )

    if created or student.mentor is None:
        # Student is new or mentor not set
        return redirect('student:assign_mentor')

    # Load student marks, etc.
    marks = student.marks.select_related('course')
    return render(request, "student/student_dashboard.html", {
        "student": student,
        "marks": marks,
        "mentor": student.mentor,
    })
    
@login_required
def assign_mentor(request):
    user = request.user
    student = Student.objects.get(user=user)

    mentors = Mentor.objects.all()

    if request.method == "POST":
        mentor_id = request.POST.get("mentor")

        try:
            selected_mentor = Mentor.objects.get(user__id=mentor_id)

            # validate mentor selection
            if student.mentor and student.mentor.id != selected_mentor.id:
                messages.error(request, "❌ Wrong mentor selected! Please choose the correct mentor.")
                return redirect("student:assign_mentor")

            
            student.mentor = selected_mentor
            student.save()

            messages.success(request, "✅ Mentor assigned successfully!")
            return redirect("student:student_dashboard")

        except Mentor.DoesNotExist:
            messages.error(request, "Invalid mentor selected.")

    return render(request, "student/assign_mentor.html", {
        "student": student,
        "mentors": mentors,
    })
