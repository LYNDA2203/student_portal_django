import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from mentor.models import Student, Mark, Mentor
from courses.models import CourseTrack, Course


@pytest.mark.django_db
def test_course_track_create():
    client = APIClient()
    data = {"title": "Python Track", "description": "Basics to Advanced"}

    res = client.post("/api/tracks/", data, format="json")

    assert res.status_code == 201
    assert CourseTrack.objects.count() == 1


@pytest.mark.django_db
def test_student_list_api():
    user = User.objects.create(username="test_student")
    Student.objects.create(user=user, full_name="Test Student")

    client = APIClient()
    response = client.get("/api/students/")

    assert response.status_code == 200
    assert response.data[0]["full_name"] == "Test Student"


@pytest.mark.django_db
def test_marks_endpoint():
    u = User.objects.create(username="abc")
    student = Student.objects.create(user=u, full_name="ABC")

    track = CourseTrack.objects.create(title="Django")
    course = Course.objects.create(track=track, name="Web Dev")

    Mark.objects.create(student=student, course=course, marks_obtained=80, max_marks=100)

    client = APIClient()
    res = client.get("/api/marks/")

    assert res.status_code == 200
    assert res.data[0]["marks_obtained"] == 80


@pytest.mark.django_db
def test_mark_creation_requires_authentication():
    u = User.objects.create(username="mentor1")
    student = Student.objects.create(user=u, full_name="Mentor One")

    track = CourseTrack.objects.create(title="Django")
    course = Course.objects.create(track=track, name="Web Dev")

    client = APIClient()
    data = {"student": student.id, "course": course.id, "marks_obtained": 85, "max_marks": 100}

    response = client.post("/api/marks/", data, format="json")
    assert response.status_code == 401  # Unauthenticated


@pytest.mark.django_db
def test_mentor_can_update_marks():
    # Create mentor user
    mentor_user = User.objects.create_user(username="mentor2", password="pass123")
    mentor_user.userprofile.role = "mentor"
    mentor_user.userprofile.save()

    mentor = Mentor.objects.create(user=mentor_user, full_name="Mentor Two")

    # Create student
    student_user = User.objects.create_user(username="student2", password="pass123")
    student = Student.objects.create(user=student_user, full_name="Student Two", mentor=mentor)

    track = CourseTrack.objects.create(title="Python")
    course = Course.objects.create(track=track, name="Basics")

    mark = Mark.objects.create(student=student, course=course, marks_obtained=70, max_marks=100)

    client = APIClient()
    client.force_authenticate(user=mentor_user)

    update_data = {"marks_obtained": 95}

    response = client.patch(f"/api/marks/{student.name}/", update_data, format="json")

    assert response.status_code == 200
    mark.refresh_from_db()
    assert mark.marks_obtained == 95
    
    
@pytest.mark.django_db
def test_student_cannot_update_marks():
    student_user = User.objects.create_user(username="studX", password="pass123")
    student_user.userprofile.role = "student"
    student_user.userprofile.save()

    student = Student.objects.create(user=student_user, full_name="Stud X")

    track = CourseTrack.objects.create(title="Java")
    course = Course.objects.create(track=track, name="Core Java")

    mark = Mark.objects.create(student=student, course=course, marks_obtained=60, max_marks=100)

    client = APIClient()
    client.force_authenticate(user=student_user)

    response = client.patch(f"/api/marks/{student.name}/", {"marks_obtained": 80}, format="json")

    assert response.status_code == 403

@pytest.mark.django_db
def test_mentor_can_delete_marks():
    mentor_user = User.objects.create_user(username="mentor3", password="pass123")
    mentor_user.userprofile.role = "mentor"
    mentor_user.userprofile.save()

    mentor = Mentor.objects.create(user=mentor_user, full_name="Mentor Three")

    stu_user = User.objects.create_user(username="student3", password="pass123")
    student = Student.objects.create(user=stu_user, full_name="Student Three", mentor=mentor)

    track = CourseTrack.objects.create(title="C")
    course = Course.objects.create(track=track, name="C Basics")

    mark = Mark.objects.create(student=student, course=course, marks_obtained=50, max_marks=100)

    client = APIClient()
    client.force_authenticate(user=mentor_user)

    response = client.delete(f"/api/marks/{student.name}/")

    assert response.status_code == 204
    assert Mark.objects.count() == 0

@pytest.mark.django_db
def test_student_cannot_delete_marks():
    student_user = User.objects.create_user(username="studY", password="pass123")
    student_user.userprofile.role = "student"
    student_user.userprofile.save()

    student = Student.objects.create(user=student_user, full_name="Stud Y")

    track = CourseTrack.objects.create(title="C++")
    course = Course.objects.create(track=track, name="OOP")

    mark = Mark.objects.create(student=student, course=course, marks_obtained=75, max_marks=100)

    client = APIClient()
    client.force_authenticate(user=student_user)

    response = client.delete(f"/api/marks/{student.name}/")

    assert response.status_code == 403
