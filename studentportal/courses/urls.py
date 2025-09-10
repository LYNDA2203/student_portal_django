from django.contrib import admin
from django.urls import path
from .views import TrackListView, TrackDetailView
from django.contrib.auth.decorators import login_required

app_name = 'courses'

urlpatterns = [
    path('tracks/', login_required(TrackListView.as_view()), name='track_list'),
    path('tracks/<int:pk>/', TrackDetailView.as_view(), name='track_detail'),
]