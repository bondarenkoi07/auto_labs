from django.utils.text import slugify
from django.views.generic import UpdateView

from main.forms import UploadFileForm
from main.github_api.api import *
from main.models import *


class Group(UpdateView):
    model = Group


class TaskUpdateDescription(UpdateView):
    model = Task


class TaskSend(UpdateView):
    model = Task
    form_class = UploadFileForm


class ActionFile(UpdateView):
    model = ActionFile


class Subject(UpdateView):
    model = Subject
