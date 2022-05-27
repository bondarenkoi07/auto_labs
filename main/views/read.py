from django.views.generic import DetailView, ListView

from main.models import *


class Group(DetailView):
    model = Group


class Task(DetailView):
    model = Task


class ActionFile(DetailView):
    model = ActionFile


class Subject(DetailView):
    model = Subject


class ListGroup(ListView):
    model = Group


class ListTask(ListView):
    model = Task


class ListActionFile(ListView):
    model = ActionFile


class ListSubject(ListView):
    model = Subject
