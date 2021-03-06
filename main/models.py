from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.template.defaultfilters import slugify as django_slugify

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


# Create your models here.
class UserManager(BaseUserManager):
    """
    Custom user model manager where GitHub token is  used as password.
    """

    def create_user(self, username, token, **extra_fields):
        """
        Create and save a User with the given username and token.
        """
        if not username or not token:
            raise ValueError("The Email must be set")
        user = self.model(username, **extra_fields)
        user.token = token
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class Group(models.Model):
    year = models.PositiveSmallIntegerField(verbose_name="дата создания")
    number = models.PositiveSmallIntegerField(verbose_name="номер группы")
    course = models.PositiveSmallIntegerField(verbose_name="курс группы")
    faculty = models.PositiveSmallIntegerField(verbose_name="факультет группы")

    studing_form_variant = [
        ("О", "Очно"),
        ("З", "Заочно"),
    ]

    studing_form = models.CharField(
        max_length=2,
        choices=studing_form_variant,
        default="st",
        verbose_name="форма обучения",
    )

    def __str__(self):
        return "М%d%s-%d%dБ-%d" % (self.faculty, self.studing_form, self.course, self.number, self.year)


class GitHubUser(AbstractUser):
    username = models.CharField(verbose_name="логин", unique=True, max_length=256)
    token = models.CharField(max_length=256)
    ROLES = [
        ("st", "Ученик"),
        ("tc", "Учитель"),
        ("md", "Модератор"),
    ]

    group = models.ForeignKey(
        to=Group, verbose_name="группа", on_delete=models.DO_NOTHING, default=3
    )

    def __str__(self):
        return self.username

    objects = UserManager()

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
        to=GitHubUser,
        on_delete=models.DO_NOTHING,
        verbose_name="преподаватель",
        null=True,
    )
    name = models.CharField(verbose_name="название предмета", max_length=128)
    group = models.ManyToManyField(to=Group, verbose_name="группа")

    def __str__(self):
        return self.name


class Action(models.Model):
    name = models.CharField(verbose_name="action name", max_length=32)
    file = models.FileField(verbose_name="action file")

    def __str__(self):
        return self.name


class Task(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, verbose_name="Предмет"
    )
    input = models.FileField(verbose_name="Тестовый список входных параметров")
    output = models.FileField(verbose_name="Тестовый список ответов")
    name = models.CharField(verbose_name="Название репозитория (англ.)", max_length=128)
    description = models.CharField(verbose_name="тех. задание", max_length=1023)
    actions_file = models.ForeignKey(
        Action,
        on_delete=models.DO_NOTHING,
        verbose_name="файл с настройками проверки (.yaml)",
    )

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    user = models.ForeignKey(
        GitHubUser, on_delete=models.DO_NOTHING, verbose_name="пользователь"
    )
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, verbose_name="задание")
    status = models.CharField(verbose_name="status", max_length=32)
