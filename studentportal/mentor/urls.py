# mentor/urls.py
from django.urls import path
from . import views

app_name = 'mentor'

urlpatterns = [
    path('student/<int:student_id>/marks/', views.student_marks_view, name='student_marks'),
    path('student/<int:student_id>/course/<int:course_id>/marks/', views.student_course_marks_view, name='student_course_marks'),
]
