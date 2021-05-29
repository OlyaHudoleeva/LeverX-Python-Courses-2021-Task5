from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import *


class UserCreateSerializer(UserSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'role')


# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = '__all__'
#
#
# class TeacherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teacher
#         fields = '__all__'
#
#
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
#
#
# class LectureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lecture
#         fields = '__all__'
#
#
# class HomeworkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Homework
#         fields = '__all__'
#
#
# class StudentsToHomeworksSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StudentsToHomeworks
#         fields = '__all__'
