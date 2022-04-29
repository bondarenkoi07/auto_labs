from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Group(models.Model):
    year = models.DateField(verbose_name="дата создания")
    number = models.PositiveSmallIntegerField(verbose_name="номер группы")
    course = models.PositiveSmallIntegerField(verbose_name="курс группы")


class User(AbstractUser):
    username = models.TextField(verbose_name="логин", unique=True, max_length=256)
    token = models.TextField(max_length=256)
    pass


class Assignee(User):
    pass


class Student(User):
    pass


class Moderate(User):
    pass


class Subject(models.Model):
    assignee = models.ForeignKey(
        Assignee, on_delete=models.DO_NOTHING, verbose_name="преподаватель", null=True
    )
    course = models.PositiveSmallIntegerField(verbose_name="курс группы")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, verbose_name="группа", null=True
    )
    pass


class Task(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="задание"
    )
    pass
