from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.text import slugify
from django.views.generic import DetailView, ListView

from main.forms import UploadFileForm
from main.github_api.api import is_repo_exists, create_repo, create_or_update_content, get_last_pipeline
from main import models


class Group(DetailView):
    model = models.Group


class Task(DetailView):
    model = models.Task
    template_name = "detail/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UploadFileForm
        res = get_last_pipeline(
            request=self.request,
            repo_name=slugify(self.object.name),
            workflow_id=self.object.actions_file.file.name
        )
        if res.status_code == 200:
            context['status'] = res.json()['status']

        return context


class User(DetailView):
    model = models.GitHubUser
    template_name = "detail/profile.html"


class Action(DetailView):
    model = models.Action


class Subject(DetailView):
    model = models.Subject


class ListGroup(ListView):
    model = models.Group
    template_name = "list/group.html"


class ListTask(ListView):
    model = models.Task
    template_name = "list/task.html"


class ListActionFile(ListView):
    model = models.Action
    template_name = "list/action.html"


class ListSubject(ListView):
    model = models.Subject
    template_name = "list/subject.html"
