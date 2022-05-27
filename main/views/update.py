from django.views.generic import UpdateView
from main.models import *


class Group(UpdateView):
    model = Group


class Task(UpdateView):
    model = Task


class ActionFile(UpdateView):
    model = ActionFile


class Subject(UpdateView):
    model = Subject
