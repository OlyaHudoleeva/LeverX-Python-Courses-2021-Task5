from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Student, Teacher, User, Lecture, Homework, UsersToHomeworks
from .permissions import IsTeacherOrReadOnly, IsStudentOrReadOnly
from .serializers import CourseSerializer, UserCreateSerializer, LectureSerializer, HomeworkSerializer, \
    StudentsToHomeworksSerializer


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


class HomeworkToLectureAddition(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def post(self, request):
        serializer_hw = HomeworkSerializer(data={'description': request.data['description'],
                                                 'lecture_id': Lecture.objects.get(id=request.data['lecture_id'],
                                                                                   course_id__user_id=request.user.id).id})
        if serializer_hw.is_valid():
            serializer_hw.save()
            related_course = Lecture.objects.get(id=request.data['lecture_id']).course_id
            related_users = related_course.user_id.all()

            for user in related_users:
                if user.role == User.STUDENT:
                    new_students_to_homeworks = UsersToHomeworks.objects.create(status=UsersToHomeworks.NOT_COMPLETED,
                                                                                user_id=user,
                                                                                homework_id=serializer_hw.instance)
                    new_students_to_homeworks.save()

                elif user.role == User.TEACHER:
                    new_students_to_homeworks = UsersToHomeworks.objects.create(user_id=user,
                                                                                homework_id=serializer_hw.instance)
                    new_students_to_homeworks.save()

            return Response(serializer_hw.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_hw.errors, status=status.HTTP_400_BAD_REQUEST)


class LectureHomeworksList(APIView):

    def get(self, request, pk):
        lecture_homeworks = Homework.objects.filter(lecture_id=pk, lecture_id__course_id__user_id=request.user.id)
        if lecture_homeworks:
            serializer_obj = HomeworkSerializer(lecture_homeworks, many=True)
            return Response(serializer_obj.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentHomeworksList(APIView):
    permission_classes = [IsStudentOrReadOnly]

    def get(self, request):
        student_homeworks = Homework.objects.filter(lecture_id__course_id__user_id=request.user.id)
        if student_homeworks:
            serializer_obj = HomeworkSerializer(student_homeworks, many=True)
            return Response(serializer_obj.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentHomeworkFinishing(APIView):
    permission_classes = [IsStudentOrReadOnly]

    def post(self, request):
        serialized_obj = StudentsToHomeworksSerializer(
            data={'status': 'C', 'student_id': Student.objects.get(id=request.user.id).id,
                  'homework_id': Homework.objects.get(id=request.data['homework_id'],
                                                      lecture_id__course_id__user_id=request.user.id).id})
        if serialized_obj.is_valid():
            serialized_obj.save()
            return Response(serialized_obj.data, status=status.HTTP_201_CREATED)
        return Response(serialized_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class CompletedStudentsHomeworksList(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get(self, request):
        teacher_users_to_homeworks = UsersToHomeworks.objects.filter(user_id=request.user.id)
        teacher_homeworks = []
        for teacher_homework in teacher_users_to_homeworks:
            homework = Homework.objects.get(id=teacher_homework.homework_id_id)
            completed_by = UsersToHomeworks.objects.filter(homework_id_id=homework.id, status=UsersToHomeworks.COMPLETED)
            students = []
            for user_to_homework in completed_by:
                student = User.objects.get(id=user_to_homework.user_id_id)
                students.append({'id': student.id, 'first_name': student.first_name, 'last_name': student.last_name})
            teacher_homeworks.append({'id': homework.id, 'description': homework.description, 'students': students})

        return Response(teacher_homeworks, status=status.HTTP_200_OK)
