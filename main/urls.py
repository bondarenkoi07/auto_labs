from django.urls import path

from main.github_api import api
from main.views.create import create
from main.views.read import read
from main.views.update import update

urlpatterns = [
    path("", read.ListTask.as_view(), name="index"),
    # user auth
    path("login/", api.login, name="login"),
    path("callback/", api.callback),
    # api
    path("createrepo/<str:repo_name>/", api.create_repo, name="create-repo"),
    path("update_file/<int:tid>", update.update_task, name="send-file"),
    # Create
    path("subject/create/", create.Subject.as_view(), name="create-subject"),
    path("task/create/", create.Task.as_view(), name="create-task"),
    path("action/create/", create.ActionFile.as_view(), name="create-action"),
    path("group/create/", create.Group.as_view(), name="create-group"),
    # Read
    path("subject/read/<int:pk>/", read.Subject.as_view(), name="read-subject"),
    path("task/read/<int:pk>/", read.Task.as_view(), name="read-task"),
    path("action/read/<int:pk>/", read.Action.as_view(), name="read-action"),
    path("group/read/<int:pk>/", read.Group.as_view(), name="read-group"),
    path("profile/<int:pk>/", read.User.as_view(), name="profile"),
    # List
    path("subject/list/", read.ListSubject.as_view(), name="list-subject"),
    path("task/list/", read.ListTask.as_view(), name="list-task"),
    path("action/list/", read.ListActionFile.as_view(), name="list-action"),
    path("group/list/", read.ListGroup.as_view(), name="list-group"),
    # Update
    path("subject/update/<int:pk>/", update.Subject.as_view(), name="update-subject"),
    path("task/update/<int:pk>/", update.Task.as_view(), name="update-task"),
    path("action/update/<int:pk>/", update.Action.as_view(), name="update-action"),
    path("group/update/<int:pk>/", update.Group.as_view(), name="update-group"),
    path("user/update/<int:pk>/", update.User.as_view(), name="update-user"),
]
