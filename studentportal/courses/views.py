from django.views import generic
from django.db.models import Avg,F
from .models import CourseTrack
from mentor.models import Mark,Student
from django.contrib.auth.mixins import LoginRequiredMixin

# class TrackListView(LoginRequiredMixin,generic.ListView):
#     model = CourseTrack
#     template_name = 'course/track_list.html'
#     context_object_name = 'tracks'
    
class TrackListView(LoginRequiredMixin, generic.ListView):
    model = CourseTrack
    template_name = 'course/track_list.html'
    context_object_name = 'tracks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_id'] = self.request.user.id

        # students with overall >= 60%
        high_scorers = Student.objects.annotate(
            avg_percentage=Avg(F('marks__marks_obtained') * 100.0 / F('marks__max_marks'))
        ).filter(avg_percentage__gte=60)

        context['high_scorers'] = high_scorers
        return context
    
    
    
class TrackDetailView(generic.DetailView):
    model = CourseTrack
    template_name = 'course/track_detail.html'
    context_object_name = 'track'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        track = self.get_object()
        courses_in_track = track.courses.all()
        enrollments = Mark.objects.filter(course__in=courses_in_track).select_related("student","course")
        context["marks"] = enrollments
        return context