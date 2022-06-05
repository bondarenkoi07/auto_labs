from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import UpdateView

import main.models
from main.forms import *
from main.github_api.api import *


class User(UpdateView):
    model = GitHubUser
    template_name = "form/user.html"

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.pk})


class Group(UpdateView):
    model = main.models.Group
    form_class = GroupForm
    template_name = "form/group.html"

    def get_success_url(self):
        return reverse("read-group", kwargs={"pk": self.object.pk})


class Task(UpdateView):
    model = main.models.Task
    form_class = TaskForm
    template_name = "form/task.html"

    def get_success_url(self):
        return reverse("read-task", kwargs={"pk": self.object.pk})


class Action(UpdateView):
    model = main.models.Action
    form_class = SubjectForm
    template_name = "form/action.html"

    def get_success_url(self):
        return reverse("read-action", kwargs={"pk": self.object.pk})


class Subject(UpdateView):
    model = main.models.Subject
    form_class = SubjectForm
    template_name = "form/subject.html"

    def get_success_url(self):
        return reverse("read-subject", kwargs={"pk": self.object.pk})


@method_decorator(login_required)
def update_task(request: HttpRequest, tid: int):
    if request.user.role != "st":
        return redirect("main")
    task = main.models.Task.objects.get(id=tid)
    form = UploadFileForm(request.POST, request.FILES)

    if not form.is_valid():
        return redirect(task)

    if not is_repo_exists(request, slugify(task.name)):
        res = create_repo(request, slugify(task.name))
        if res.status_code != 200:
            request.session["error_old"] = res.json()["message"]
            return redirect(task)
        actform = UploadFileForm()
        actform.file = task.actions_file.file
        actform.title = "test.yml"
        res = create_or_update_content(
            request=request, repo_name=slugify(task.name), form=actform
        )

        if res != "ok":
            request.session["error_old"] = res
            return redirect(task)

        actform = UploadFileForm()
        actform.file = task.input.file
        actform.title = task.input.name

        res = create_or_update_content(
            request=request, repo_name=slugify(task.name), form=actform
        )

        if res != "ok":
            request.session["error_old"] = res
            return redirect(task)

        actform = UploadFileForm()
        actform.file = task.output.file
        actform.title = task.output.name

        res = create_or_update_content(
            request=request, repo_name=slugify(task.name), form=actform
        )

        if res != "ok":
            request.session["error_old"] = res
            return redirect(task)

    res = create_or_update_content(
        request=request, repo_name=slugify(task.name), form=form
    )
    if res != "ok":
        request.session["error_old"] = res

    return reverse("read-subject", kwargs={"pk": task.pk})
