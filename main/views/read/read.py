from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from main import models
from main.forms import UploadFileForm
from main.github_api.api import get_last_pipeline


@method_decorator(login_required, name='dispatch')
class Group(DetailView):
    model = models.Group
    template_name = 'detail/group.html'


@method_decorator(login_required, name='dispatch')
class Task(DetailView):
    model = models.Task
    template_name = "detail/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UploadFileForm
        res = get_last_pipeline(
            request=self.request,
            repo_name=models.slugify(self.object.name),
            workflow_id=self.object.actions_file.file.name
        )

        print(res.status_code)

        if res.status_code == 200:
            print(res.json()['workflow_runs'][0]['conclusion'])
            context['conclusion'] = res.json()['workflow_runs'][0]['conclusion']
            print(res.json()['workflow_runs'][0]['status'])
            context['status'] = res.json()['workflow_runs'][0]['status']

        return context


@method_decorator(login_required, name='dispatch')
class User(DetailView):
    model = models.GitHubUser
    template_name = "detail/profile.html"


@method_decorator(login_required, name='dispatch')
class Action(DetailView):
    model = models.Action
    template_name = 'detail/action.html'


@method_decorator(login_required, name='dispatch')
class Subject(DetailView):
    model = models.Subject
    template_name = 'detail/subject.html'


@method_decorator(login_required, name='dispatch')
class ListGroup(ListView):
    model = models.Group
    template_name = "list/group.html"


@method_decorator(login_required, name='dispatch')
class ListTask(ListView):
    model = models.Task
    template_name = "list/task.html"


@method_decorator(login_required, name='dispatch')
class ListActionFile(ListView):
    model = models.Action
    template_name = "list/action.html"


@method_decorator(login_required, name='dispatch')
class ListSubject(ListView):
    model = models.Subject
    template_name = "list/subject.html"
