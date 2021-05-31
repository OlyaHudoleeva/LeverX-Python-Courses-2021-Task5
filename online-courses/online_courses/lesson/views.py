from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Student, Teacher
from .permissions import IsTeacherOrReadOnly
from .serializers import CourseSerializer, UserCreateSerializer


class UserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer_obj = UserCreateSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            if serializer_obj.data.get('role') == 'T':
                new_teacher = Teacher.objects.create(id=serializer_obj.instance)
                new_teacher.save()
            elif serializer_obj.data.get('role') == 'S':
                new_student = Student.objects.create(id=serializer_obj.instance)
                new_student.save()
            return Response(serializer_obj.data, status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseList(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get(self, request):
        courses = Course.objects.all()
        serializer_obj = CourseSerializer(courses, many=True)
        return Response(serializer_obj.data)

    def post(self, request):
        serializer_obj = CourseSerializer(
            data={'name': request.data['name'], 'description': request.data['description'],
                  'period_from': request.data['period_from'], 'period_to': request.data['period_to'],
                  'user_id': [self.request.user.id]})
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data, status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        course = self.get_object(pk)
        serialized_obj = CourseSerializer(course)
        return Response(serialized_obj.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        serialized_course = CourseSerializer(course, data=request.data)
        if serialized_course.is_valid():
            serialized_course.save()
            return Response(serialized_course.data, status=status.HTTP_200_OK)
        return Response(serialized_course.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
