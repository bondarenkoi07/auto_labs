from django.views.generic import CreateView

from main.models import *


class Group(CreateView):
    model = Group


class Task(CreateView):
    model = Task


class ActionFile(CreateView):
    model = ActionFile


class Subject(CreateView):
    model = Subject

