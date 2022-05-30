from django.urls import path, reverse

from main.github_api import api

urlpatterns = [
    path("login/", api.login),
    path("callback/", api.callback),
    path("user/", api.user_info, name="account"),
    path("createrepo/<str:repo_name>/", api.create_repo, name="create-repo"),
]
