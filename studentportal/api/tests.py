import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from mentor.models import Student,Mark
from course.models import CourseTrack,Course

@pytest.mark.django_db
def test_course_track_create():
    client = APIClient()
    data = {"title": "Python Track", "description": "Basics to Advanced"}

    res = client.post("/api/coursetracks/", data, format="json")

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
    course = Course.objects.create(track=track)
    Mark.objects.create(student=student, course=course, marks_obtained=80, max_marks=100)

    client = APIClient()
    res = client.get("/api/marks/")

    assert res.status_code == 200
    assert res.data[0]["marks_obtained"] == 80