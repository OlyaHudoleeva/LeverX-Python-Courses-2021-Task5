from django.urls import path, include

from lesson import views

# from lesson.router import router

urlpatterns = [
    # path('', include(router.urls)),
    path('auth/registration', views.UserRegistration.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('courses/', views.CourseList.as_view()),
    path('courses/<int:pk>', views.CourseDetail.as_view()),
    path('add/user/course/<int:pk>', views.UserToCourseAddition.as_view()),
    path('delete/user/course/<int:pk>', views.UserFromCourseRemover.as_view()),
    path('student/courses/list', views.StudentCoursesList.as_view()),
    path('course/lectures/', views.LectureList.as_view()),
    path('course/lectures/<int:pk>', views.LectureDetail.as_view()),
    path('user/course/<int:pk>/lectures/list/', views.CourseLecturesList.as_view()),
    path('course/lecture/homework/add', views.HomeworkToLectureAddition.as_view()),
    path('user/course/lecture/<int:pk>/homeworks/list', views.LectureHomeworksList.as_view()),
    path('student/homeworks/list', views.StudentHomeworksList.as_view()),
    path('student/homework/complete', views.StudentHomeworkFinishing.as_view()),
    path('homeworks/completed/list', views.CompletedStudentsHomeworksList.as_view())

]
