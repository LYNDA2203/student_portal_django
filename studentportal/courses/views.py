from django.views import generic
from .models import CourseTrack
from django.contrib.auth.mixins import LoginRequiredMixin

class TrackListView(LoginRequiredMixin,generic.ListView):
    model = CourseTrack
    template_name = 'course/track_list.html'
    context_object_name = 'tracks'

class TrackDetailView(generic.DetailView):
    model = CourseTrack
    template_name = 'course/track_detail.html'
    context_object_name = 'track'