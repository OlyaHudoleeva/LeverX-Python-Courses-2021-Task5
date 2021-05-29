from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *



# class UserAPI(viewsets.ModelViewSet):
#     serializer_class = UserCreateSerializer
#     queryset = User.objects.all()


# class StudentAPI(viewsets.ModelViewSet):
#     serializer_class = StudentSerializer
#     queryset = Student.objects.all()
#
#
# class TeacherAPI(viewsets.ModelViewSet):
#     serializer_class = TeacherSerializer
#     queryset = Teacher.objects.all()

# @api_view(['GET'])
# def course_list(request):
#     courses = Course.objects.all()
#     serializer = CourseSerializer(courses, many=True)
#     return Response(serializer.data)


# class CourseAPI(viewsets.ModelViewSet):
#     serializer_class = CourseSerializer
#     queryset = Course.objects.all()
#
#
# class LectureAPI(viewsets.ModelViewSet):
#     serializer_class = LectureSerializer
#     queryset = Lecture.objects.all()
#
#
# class HomeworkAPI(viewsets.ModelViewSet):
#     serializer_class = HomeworkSerializer
#     queryset = Homework.objects.all()

#
# class StudentsToHomeworksAPI(viewsets.ModelViewSet):
#     serializer_class = StudentsToHomeworksSerializer
#     queryset = StudentsToHomeworks.objects.all()
