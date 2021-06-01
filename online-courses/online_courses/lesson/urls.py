from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from lesson import views
# from lesson.router import router

urlpatterns = [
    # path('', include(router.urls)),
    path('auth/registration', views.UserRegistration.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('courses/', views.CourseList.as_view()),
    path('courses/<int:pk>', views.CourseDetail.as_view()),
    path('add/user/course/<int:pk>', views.UserToCourseAddition.as_view()),
    path('delete/user/course/<int:pk>', views.UserFromCourseRemover.as_view())
]