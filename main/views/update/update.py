from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import UpdateView


from main.github_api.api import *
from main import models


class Group(UpdateView):
    model = models.Group


class TaskUpdateDescription(UpdateView):
    model = models.Task


class TaskSend(UpdateView):
    model = models.Task
    form_class = UploadFileForm


class ActionFile(UpdateView):
    model = models.Action


class Subject(UpdateView):
    model = models.Subject


@method_decorator(login_required)
def update_task(request: HttpRequest, tid: int):
    if request.user.role != "st":
        return redirect("main")
    task = models.Task.objects.get(id=tid)
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

    res = create_or_update_content(
        request=request, repo_name=slugify(task.name), form=form
    )
    if res != "ok":
        request.session["error_old"] = res
        return redirect(task)

    return redirect(task)
