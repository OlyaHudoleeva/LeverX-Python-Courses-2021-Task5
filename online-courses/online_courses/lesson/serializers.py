from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import *


class UserCreateSerializer(UserSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'role')
        depth = 1


# class StudentSerializer(serializers.ModelSerializer):
#     id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='S'))
#     class Meta:
#         model = Student
#         fields = '__all__'
#
#
# class TeacherSerializer(serializers.ModelSerializer):
#     id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='T'))
#     class Meta:
#         model = Teacher
#         fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Course
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'
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
