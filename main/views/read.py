from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.text import slugify
from django.views.generic import DetailView, ListView

from main.forms import UploadFileForm
from main.github_api.api import is_repo_exists, create_repo, create_or_update_content
from main.models import *


class Group(DetailView):
    model = Group


class Task(DetailView):
    model = Task
    template_name = 'detail/task_detail.html'


class User(DetailView):
    model = User


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


def update_task(request: HttpRequest, tid: int):
    task = Task.objects.get(id=tid)
    form = UploadFileForm(request.POST, request.FILES)

    if not form.is_valid():
        return redirect(task)

    if not is_repo_exists(request, slugify(task.name)):
        res = create_repo(request, slugify(task.name))
        actform = UploadFileForm()
        actform.file = task.actions_file.file
        actform.title = 'test.yml'
        create_or_update_content(request=request, repo_name=slugify(task.name), form=actform)

    create_or_update_content(request=request, repo_name=slugify(task.name), form=form)



