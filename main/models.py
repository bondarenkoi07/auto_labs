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
    ROLES = [
        ("st", "Ученик"),
        ("tc", "Учитель"),
        ("md", "Модератор"),
    ]

    role = models.CharField(
        max_length=2, choices=ROLES, default="st", verbose_name="статус пользователя"
    )
    pass


class Subject(models.Model):
    assignee = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, verbose_name="преподаватель", null=True
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
    right_output = models.FileField(verbose_name="Тестовый список ответов")
    input = models.FileField(verbose_name="Тестовый список входных параметров")
    name = models.TextField(verbose_name="название репозитория (англ.)")
    actions_file = models.FileField(verbose_name="файл с настройками проверки (.yaml)")
    pass


class ActionFile(models.Model):
    name = models.CharField(verbose_name="action name")
    file = models.FileField(verbose_name="action file")
