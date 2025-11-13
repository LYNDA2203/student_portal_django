from django.urls import path
from . import views

app_name= 'student'

urlpatterns = [
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path('assign_mentor/', views.assign_mentor, name='assign_mentor'),
]