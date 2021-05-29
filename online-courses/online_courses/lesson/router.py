from rest_framework import routers

from lesson.viewsets import CourseViewSet

router = routers.DefaultRouter()
router.register('courses', CourseViewSet)
