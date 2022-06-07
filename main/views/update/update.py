from django.contrib.auth.decorators import login_required
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
    form_class = ActionFileForm
    template_name = "form/action.html"

    def get_success_url(self):
        return reverse("read-action", kwargs={"pk": self.object.pk})


class Subject(UpdateView):
    model = main.models.Subject
    form_class = SubjectForm
    template_name = "form/subject.html"

    def get_success_url(self):
        return reverse("read-subject", kwargs={"pk": self.object.pk})


@login_required
def update_task(request: HttpRequest, tid: int):
    if request.user.role != "st":
        return HttpResponseRedirect(reverse("main"))
    task = main.models.Task.objects.get(id=tid)
    form = UploadFileForm(request.POST, request.FILES)

    if not form.is_valid():
        return HttpResponseRedirect(reverse("read-task", kwargs={"pk": task.pk}))

    if not is_repo_exists(request, slugify(task.name)):
        res = create_repo(request, slugify(task.name))
        if res.status_code != 201:
            print(res.status_code)
            request.session["error_old"] = res.json()["message"]
            return HttpResponseRedirect(reverse("read-task", kwargs={"pk": task.pk}))

    file = task.actions_file.file

    res = create_or_update_action(
        request=request, repo_name=slugify(task.name), file=file
    )

    if res != "ok":
        request.session["error_old"] = res + " action file"
        return HttpResponseRedirect(reverse("read-task", kwargs={"pk": task.pk}))

    file = task.input.file

    res = create_or_update_content(
        request=request, repo_name=slugify(task.name), file=file
    )

    if res != "ok":
        request.session["error_old"] = res + " input file"
        return HttpResponseRedirect(reverse("read-task", kwargs={"pk": task.pk}))

    file = task.output.file
    res = create_or_update_content(
        request=request, repo_name=slugify(task.name), file=file
    )

    if res != "ok":
        request.session["error_old"] = res + " output file"
        return HttpResponseRedirect(reverse("read-task", kwargs={"pk": task.pk}))

    res = create_or_update_content(
        request=request, repo_name=slugify(task.name), file=request.FILES['file']
    )
    if res != "ok":
        request.session["error_old"] = res
    else:
        request.session["error_old"] = None

    return HttpResponseRedirect(reverse("read-task", kwargs={"pk": task.pk}))
