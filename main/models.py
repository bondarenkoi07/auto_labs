from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from main.managers import UserManager


class Group(models.Model):
    year = models.DateField(verbose_name="дата создания")
    number = models.PositiveSmallIntegerField(verbose_name="номер группы")
    course = models.PositiveSmallIntegerField(verbose_name="курс группы")


class User(AbstractUser):
    username = models.CharField(verbose_name="логин", unique=True, max_length=256)
    token = models.CharField(max_length=256)
    ROLES = [
        ("st", "Ученик"),
        ("tc", "Учитель"),
        ("md", "Модератор"),
    ]

    objects = UserManager

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    role = models.CharField(
        max_length=2, choices=ROLES, default="st", verbose_name="статус пользователя"
    )
    pass


class Subject(models.Model):
    assignee = models.ForeignKey(
        to=User, on_delete=models.DO_NOTHING, verbose_name="преподаватель", null=True
    )
    name = models.CharField(verbose_name="название предмета")
    group = models.ManyToManyField(
        to=Group, on_delete=models.CASCADE, verbose_name="группа", null=True
    )
    pass


class ActionFile(models.Model):
    name = models.CharField(verbose_name="action name")
    file = models.FileField(verbose_name="action file")


class Task(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="задание"
    )
    input = models.FileField(verbose_name="Тестовый список входных параметров")
    right_output = models.FileField(verbose_name="Тестовый список ответов")
    name = models.CharField(verbose_name="название репозитория (англ.)")
    description = models.CharField(verbose_name="тех. задание")
    actions_file = models.ForeignKey(
        ActionFile,
        on_delete=models.CASCADE,
        verbose_name="файл с настройками проверки (.yaml)",
    )


class TaskStatus(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,verbose_name="пользователь"
    )
    task = models.ForeignKey(
        Task, on_delete=models.DO_NOTHING, verbose_name="задание"
    )
    status = models.CharField(verbose_name="status")