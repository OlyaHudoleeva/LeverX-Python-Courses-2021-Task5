from django.urls import path, include

from lesson import views

# from lesson.router import router

urlpatterns = [
    path('auth/registration', views.UserRegistration.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('courses/', views.CourseList.as_view()),
    path('courses/<int:pk>', views.CourseDetail.as_view()),
    path('courses/<int:pk>/user/add', views.UserToCourseAddition.as_view()),
    path('courses/<int:pk>/user/delete', views.UserFromCourseRemover.as_view()),
    path('student/courses', views.StudentCoursesList.as_view()),
    path('lectures/', views.LectureList.as_view()),
    path('lectures/<int:pk>', views.LectureDetail.as_view()),
    path('courses/<int:pk>/lectures', views.CourseLecturesList.as_view()),
    path('homeworks/add', views.HomeworkToLectureAddition.as_view()),
    path('lectures/<int:pk>/homeworks', views.LectureHomeworksList.as_view()),
    path('student/homeworks', views.StudentHomeworksList.as_view()),
    path('student/homeworks/complete', views.StudentHomeworkFinishing.as_view()),
    path('homeworks/completed', views.CompletedStudentsHomeworksList.as_view()),
    path('homeworks/rates/add', views.RateOrCommentToStudentHomeworkAddition.as_view()),
    path('homeworks/teacher-comment/add', views.RateOrCommentToStudentHomeworkAddition.as_view()),
    path('homeworks/student-comment/add', views.StudentCommentToRateAddition.as_view()),
    path('homeworks/rates', views.HomeworkRatesList.as_view())
]
