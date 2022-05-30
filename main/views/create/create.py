from django.urls import reverse
from django.views.generic import CreateView

from main.forms import *
from main import models


class Group(CreateView):
    model = models.Group
    form_class = GroupForm
    template_name = "form/group.html"

    def get_success_url(self):
        return reverse("read-group", kwargs={"pk": self.object.pk})


class Task(CreateView):
    model = models.Task
    form_class = TaskForm
    template_name = "form/task.html"

    def get_success_url(self):
        return reverse("read-task", kwargs={"pk": self.object.pk})


class ActionFile(CreateView):
    model = models.Action
    form_class = ActionFileForm
    template_name = "form/action.html"

    def get_success_url(self):
        return reverse("read-action", kwargs={"pk": self.object.pk})


class Subject(CreateView):
    model = models.Subject
    form_class = SubjectForm
    template_name = "form/subject.html"

    def get_success_url(self):
        return reverse("read-subject", kwargs={"pk": self.object.pk})
