from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    STUDENT = 'S'
    TEACHER = 'T'

    ROLES = [
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
    ]

    role = models.CharField(max_length=1, choices=ROLES)
    course_id = models.ManyToManyField('Course', related_name='user_course_id')

    REQUIRED_FIELDS = ['email', 'password', 'role']
    USERNAME_FIELD = 'username'

    def get_username(self):
        return self.username

class Student(models.Model):
    id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)


class Teacher(models.Model):
    id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    position = models.CharField(max_length=30, blank=True, null=True)


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    period_from = models.DateField(null=True, blank=True)
    period_to = models.DateField(null=True, blank=True)
    user_id = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users')


class Lecture(models.Model):
    topic = models.CharField(max_length=100)
    presentation_file = models.FileField(upload_to='uploads/')
    course_id = models.ForeignKey(Course, related_name='course_id', on_delete=models.CASCADE)


class Homework(models.Model):
    description = models.TextField()
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE)


class StudentsToHomeworks(models.Model):
    value = models.SmallIntegerField()
    student_comment = models.TextField()
    teacher_comment = models.TextField()
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)
    homework_id = models.ForeignKey(Homework, on_delete=models.PROTECT)
