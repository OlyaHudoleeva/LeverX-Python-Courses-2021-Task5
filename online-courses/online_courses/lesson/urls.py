from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from lesson import views
# from lesson.router import router

urlpatterns = [
    # path('auth/', include('rest_auth.urls')),
    # path('auth/registration/', include('rest_auth.registration.urls')),
    # path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('courses/', views.CourseList.as_view()),
    path('courses/<int:pk>', views.CourseDetail.as_view())
]