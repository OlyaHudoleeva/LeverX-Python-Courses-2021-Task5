from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Student, Teacher, User, Lecture
from .permissions import IsTeacherOrReadOnly, IsStudentOrReadOnly
from .serializers import CourseSerializer, UserCreateSerializer, LectureSerializer


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


class UserToCourseAddition(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def patch(self, request, pk):
        try:
            course = Course.objects.get(pk=pk, user_id=request.user.pk)
            if course:
                new_user = User.objects.get(id=request.data['user_id'])
                course.user_id.add(new_user)
                serializer = CourseSerializer(course)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserFromCourseRemover(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk, user_id=request.user.pk)
            if course:
                user_to_delete = User.objects.get(id=request.data['user_id'])
                course.user_id.remove(user_to_delete)
                serializer = CourseSerializer(course)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class StudentCoursesList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_courses = Course.objects.filter(user_id=request.user.id)
        if student_courses:
            serializer_obj = CourseSerializer(student_courses, many=True)
            return Response(serializer_obj.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LectureList(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def post(self, request):
        serializer_obj = LectureSerializer(
            data={'topic': request.data['topic'], 'presentation_file': request.data['presentation_file'],
                  'course_id': Course.objects.get(id=request.data['course_id']).id})
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data, status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class LectureDetail(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get_object(self, pk):
        try:
            return Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        lecture = self.get_object(pk)
        serialized_obj = LectureSerializer(lecture)
        return Response(serialized_obj.data)

    def put(self, request, pk):
        try:
            lecture = Lecture.objects.get(id=pk, course_id__user_id=request.user.id)
            serialized_lecture = LectureSerializer(lecture, data=request.data)
            if serialized_lecture.is_valid():
                serialized_lecture.save()
                return Response(serialized_lecture.data, status=status.HTTP_200_OK)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized_lecture.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            lecture = Lecture.objects.get(id=pk, course_id__user_id=request.user.id)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        lecture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseLecturesList(APIView):

    def get(self, request, pk):

        courses_lectures = Lecture.objects.filter(course_id=pk, course_id__user_id=request.user.id)
        if courses_lectures:
            serializer_obj = LectureSerializer(courses_lectures, many=True)
            return Response(serializer_obj.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



#
#
# class HomeworkAPI(viewsets.ModelViewSet):
#     serializer_class = HomeworkSerializer
#     queryset = Homework.objects.all()

#
# class StudentsToHomeworksAPI(viewsets.ModelViewSet):
#     serializer_class = StudentsToHomeworksSerializer
#     queryset = StudentsToHomeworks.objects.all()
