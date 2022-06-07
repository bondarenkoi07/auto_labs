import base64
import os

import requests
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from requests import Response

from main.github_api import BASE, RoleDict


def url_encode(url: str, kwargs: dict[str, str]) -> str:
    url += "?"
    for i in kwargs:
        url += "{}={}".format(i, kwargs[i])
        url += "&"
    url = url[: len(url) - 1]
    return url


def login(request, *args, **kwargs) -> HttpResponse:
    user_login = request.GET.get("login", "")
    data = {
        "client_id": settings.GITHUB_OAUTH_CLIENT_ID,
        "login": user_login,
        "scope": "user repo gist workflow",
    }
    url = url_encode(url="https://github.com/login/oauth/authorize", kwargs=data)
    return redirect(url)


def callback(request: HttpRequest) -> HttpResponse:
    code = request.GET.get("code", "")
    if code != "":
        data = {
            "client_id": settings.GITHUB_OAUTH_CLIENT_ID,
            "client_secret": settings.GITHUB_OAUTH_SECRET,
            "code": code,
        }

        header = {"Accept": "application/json"}

        response = requests.post(
            "https://github.com/login/oauth/access_token", data=data, headers=header
        )
        auth_token = response.json()
        request.session["GITHUB_TOKEN"] = auth_token["access_token"]
        r = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": "token %s" % request.session["GITHUB_TOKEN"],
                "Accept": "application/vnd.github.v3+json",
            },
        )

        username = r.json()["login"]
        token = request.session["GITHUB_TOKEN"]

        user = authenticate(request=request, username=username, auth_token=token)
        if user is not None:
            auth.login(request=request, user=user)
            print(user.pk)
            return HttpResponseRedirect(reverse("profile", args=[user.pk]))
        else:
            return redirect("login")
    else:
        return redirect("login")


def create_repo(request: HttpRequest, repo_name: str) -> Response:
    print(f"create_repo {request.user.token}")
    r = requests.post(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": "token %s" % request.user.token,
            "Accept": "application/vnd.github.v3+json",
        },
        json={"name": repo_name},
    )
    return r


def is_repo_exists(request: HttpRequest, repo_name: str) -> bool:
    r = requests.get(
        f"https://api.github.com/repos/{request.user.username}/{repo_name}",
        headers={
            "Authorization": "token %s" % request.user.token,
            "Accept": "application/vnd.github.v3+json",
        },
    )
    return r.status_code == 200


def add_collaborator(
        request: HttpRequest, repo_name: str, owner: str, collaborator_name: str, role: str
) -> HttpResponse:
    if repo_name == "":
        return JsonResponse({"error": "No matching repository"})

    if owner == "":
        return JsonResponse({"error": "No noticed owner"})

    if collaborator_name == "":
        return JsonResponse({"error": "Notice collaborator nickname/login"})

    permissions = RoleDict["zerg"] if role == "" else RoleDict[role]

    r = requests.put(
        f"/repos/{owner}/{repo_name}/collaborators/{collaborator_name}",
        data={"permissions": permissions},
        headers={
            "Authorization": "token %s" % request.session["GITHUB_TOKEN"],
            "Accept": "application/vnd.github.v3+json",
        },
    )

    return JsonResponse(r.json())


def create_branch(
        request: HttpRequest,
        repo_name: str,
        owner: str,
        target_branch: str,
        parent_branch: str,
) -> HttpResponse:
    if repo_name == "":
        return JsonResponse({"error": "No matching repository"})

    if owner == "":
        return JsonResponse({"error": "No noticed owner"})

    if target_branch == "":
        target_branch = f"feature/{request.user.username}"

    if parent_branch == "":
        return JsonResponse({"error": "No parent branch for new reference"})

    headers = {
        "Authorization": "token %s" % request.session["GITHUB_TOKEN"],
        "Accept": "application/vnd.github.v3+json",
    }

    branches = requests.get(
        f"https://api.github.com/repos/{owner}/{repo_name}/branches", headers=headers
    ).json()
    sha = ""
    for branch in branches:
        if branch["name"] is None:
            return JsonResponse(branches)

        if branch["name"] == parent_branch:
            sha = branch["commit"]["sha"]

    res = requests.post(
        f"https://api.github.com/repos/{owner}/{repo_name}/git/refs",
        json={"ref": f"refs/heads/{target_branch}", "sha": sha},
        headers=headers,
    )

    return JsonResponse(res.json())


def commit_file(
        request: HttpRequest, repo_name: str, target_branch: str
) -> HttpResponse:
    if repo_name == "":
        return JsonResponse({"error": "No matching repository"})
    owner = request.user.username
    if owner == "":
        return JsonResponse({"error": "No noticed owner"})

    if target_branch == "":
        return JsonResponse({"error": "No target branch for new commit"})

    if len(request.FILES) == 0:
        return JsonResponse({"error": "Nothing to commit"})

    headers = {
        "Authorization": "token %s" % request.session["GITHUB_TOKEN"],
        "Accept": "application/vnd.github.v3+json",
    }

    r = requests.get(
        f"https://api.github.com/repos/{owner}/{repo_name}/branches/{target_branch}",
        headers=headers,
    )

    if r.json()["commit"] is None:
        return JsonResponse(r.json())

    last_commit_sha = r.json()["commit"]["sha"]
    files = request.FILES.getlist("files")
    tree = []

    for f in files:
        # add blobs for files
        r = requests.post(
            f"https://api.github.com/repos/{owner}/{repo_name}/git/blobs",
            json={"content": f.read(), "encoding": "utf-8", },
            headers=headers,
        )

        if r.json()["sha"] is None:
            return JsonResponse(r.json())

        # add blob info to new VCS tree
        tree.append(
            {
                "path": BASE + f.name,
                "mode": "100644",
                "type": "blob",
                "sha": r.json()["sha"],
            }
        )

    # make new tree
    r = requests.post(
        f"https://api.github.com/repos/{owner}/{repo_name}/git/trees",
        json={"base_tree": last_commit_sha, "tree": tree},
        headers=headers,
    )

    if r.json()["sha"] is None:
        return JsonResponse(r.json())

    tree_sha = r.json()["sha"]

    # form commit
    r = requests.post(
        f"https://api.github.com/repos/{owner}/{repo_name}/git/commits",
        json={
            "message": f"auto-labs generated commit",
            "author": {"name": request.user.username, "email": request.user.email},
            "parents": [last_commit_sha],
            "tree": tree_sha,
        },
        headers=headers,
    )

    if r.json()["sha"] is None:
        return JsonResponse(r.json())

    new_commit_sha = r.json()["sha"]

    # update target branch
    r = requests.post(
        f"https://api.github.com/repos/{owner}/{repo_name}/git/commits",
        json={"ref": f"refs/heads/{target_branch}", "sha": new_commit_sha},
        headers=headers,
    )


def create_or_update_action(
        request: HttpRequest, repo_name: str, file
) -> str:
    if repo_name == "":
        return "create-repo"

    data = {}

    r = requests.get(
        f"https://api.github.com/repos/{request.user.username}/{repo_name}/contents/.github/workflows/{os.path.basename(file.name)}",
        headers={
            "Authorization": "token %s" % request.session["GITHUB_TOKEN"],
            "Accept": "application/vnd.github.v3+json",
        },
    )

    if r.status_code == 200:
        data["sha"] = r.json()["sha"]

    message = file.read()
    message_base64_bytes = base64.b64encode(message)
    message_base64 = message_base64_bytes.decode("utf-8")

    data["message"] = f"upload file {os.path.basename(file.name)}"
    data["content"] = message_base64
    print(
        f"https://api.github.com/repos/{request.user.username}/{repo_name}/contents/.github/workflows/{os.path.basename(file.name)}")
    r = requests.put(
        f"https://api.github.com/repos/{request.user.username}/{repo_name}/contents/.github/workflows/{os.path.basename(file.name)}",
        headers={
            "Authorization": "token %s" % request.user.token,
            "Accept": "application/vnd.github.v3+json",
        },
        json=data,
    )

    if r.status_code != 201 and r.status_code != 200:
        try:
            msg = r.json()["message"]
        except:
            msg = r.status_code
        return "sent file creation request: " + msg.__str__()

    return "ok"


def create_or_update_content(
        request: HttpRequest, repo_name: str, file
) -> str:
    data = {}

    r = requests.get(
        f"https://api.github.com/repos/{request.user.username}/{repo_name}/contents/{os.path.basename(file.name)}",
        headers={
            "Authorization": "token %s" % request.session["GITHUB_TOKEN"],
            "Accept": "application/vnd.github.v3+json",
        },
    )

    if r.status_code == 200:
        data["sha"] = r.json()["sha"]

    message = file.read()
    message_base64_bytes = base64.b64encode(message)
    message_base64 = message_base64_bytes.decode("utf-8")

    data["message"] = f"upload file {os.path.basename(file.name)}"
    data["content"] = message_base64
    print(f"https://api.github.com/repos/{request.user.username}/{repo_name}/contents/{os.path.basename(file.name)}")
    r = requests.put(
        f"https://api.github.com/repos/{request.user.username}/{repo_name}/contents/{os.path.basename(file.name)}",
        headers={
            "Authorization": "token %s" % request.user.token,
            "Accept": "application/vnd.github.v3+json",
        },
        json=data,
    )

    if r.status_code != 201 and r.status_code != 200:
        try:
            msg = r.json()["message"]
        except:
            msg = r.status_code
        return "sent file creation request: " + msg.__str__()

    return "ok"


def get_last_pipeline(request: HttpRequest, repo_name: str, workflow_id: str) -> Response:
    owner = request.user.username
    print(f"https://api.github.com/repos/{owner}/{repo_name}/actions/workflows/{workflow_id}/runs")
    r = requests.get(
        f"https://api.github.com/repos/{owner}/{repo_name}/actions/workflows/{workflow_id}/runs",
        headers={
            "Authorization": "token %s" % request.user.token,
            "Accept": "application/vnd.github.v3+json",
        },
    )

    return r
