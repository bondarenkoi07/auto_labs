from django.views.generic import CreateView

from main.forms import *
from main.models import *


class Group(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'create/group.html'


class Task(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'create/task.html'


class ActionFile(CreateView):
    model = ActionFile
    form_class = ActionFileForm
    template_name = 'create/action.html'


class Subject(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'create/subject.html'

