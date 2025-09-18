from django.views import generic
from .models import CourseTrack,Enrollment,CourseModule
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
        return context
    
class TrackDetailView(generic.DetailView):
    model = CourseTrack
    template_name = 'course/track_detail.html'
    context_object_name = 'track'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        track = self.get_object()  # valid here 
        context['enrollments'] = Enrollment.objects.filter(track=track).select_related('student__user')
        return context