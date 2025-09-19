from django.db import models
from django.contrib.auth.models import User

class CourseTrack(models.Model):
    
    TRACK_CHOICES = [
        ('python_fullstack', 'Python Full Stack'),
        ('ml_ai', 'ML / AI'),
        ('java_fullstack', 'Java Full Stack'),
    ]

    key = models.CharField(
        max_length=30,
        choices=TRACK_CHOICES,
        unique=True
    )
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Course Track"
        verbose_name_plural = "Course Tracks"

    def __str__(self):
        return self.get_key_display()


class CourseModule(models.Model):
    track = models.ForeignKey(CourseTrack, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['track', 'order']
        verbose_name = "Course Module"
        verbose_name_plural = "Course Modules"

    def __str__(self):
        return f"{self.track.get_key_display()} — {self.title}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # other student-specific fields

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    track = models.ForeignKey(CourseTrack, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2)  # or Integer
    # maybe other fields like date enrolled etc.

    class Meta:
        unique_together = ('student', 'track')