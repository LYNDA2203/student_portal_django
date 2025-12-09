from django.urls import path
from .views import CourseTrackViewSet,CourseViewSet,CourseModuleViewSet,StudentViewSet,MarkViewSet,MentorViewSet
from rest_framework.routers import DefaultRouter

app_name='api'

router=DefaultRouter()

router.register(r'coursetracks',CourseTrackViewSet),
router.register(r'courses',CourseViewSet),
router.register(r'coursemodules',CourseModuleViewSet),
router.register(r'students',StudentViewSet),
router.register(r'marks',MarkViewSet),
router.register(r'mentors',MentorViewSet),

urlpatterns = router.urls