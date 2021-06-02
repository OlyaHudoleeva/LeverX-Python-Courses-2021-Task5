from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STUDENT = 'S'
    TEACHER = 'T'

    ROLES = [
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
    ]

    role = models.CharField(max_length=1, choices=ROLES)

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


class UsersToHomeworks(models.Model):
    COMPLETED = 'C'
    NOT_COMPLETED = 'N'

    STATUSES = [
        (COMPLETED, 'completed'),
        (NOT_COMPLETED, 'not completed'),
    ]

    rate = models.SmallIntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUSES, blank=True, null=True)
    student_comment = models.TextField(blank=True, null=True)
    teacher_comment = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    homework_id = models.ForeignKey(Homework, on_delete=models.PROTECT, blank=True, null=True)
