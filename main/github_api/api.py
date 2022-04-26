import requests
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


def url_encode(url: str, kwargs: dict[str, str]) -> str:
    url += "?"
    for i in kwargs:
        url += "{}={}".format(i, kwargs[i])
        url += "&"
    url = url[:len(url) - 1]
    return url


def login(request, *args, **kwargs) -> HttpResponse:
    user_login = request.GET.get("login", "")
    data = {"client_id": settings.GITHUB_OAUTH_CLIENT_ID, "login": user_login, "scope": "user repo gist workflow"}
    url = url_encode(url="https://github.com/login/oauth/authorize", kwargs=data)
    return redirect(url)


def callback(request: HttpRequest) -> HttpResponse:
    code = request.GET.get("code", "")
    if code != "":
        data = {
            "client_id": settings.GITHUB_OAUTH_CLIENT_ID,
            "client_secret": settings.GITHUB_OAUTH_SECRET,
            "code": code
        }

        header = {
            "Accept": 'application/json'
        }

        response = requests.post("https://github.com/login/oauth/access_token", data=data, headers=header)
        auth_token = response.json()
        request.session["GITHUB_TOKEN"] = auth_token["access_token"]
        return redirect('account')
    else:
        return redirect('auth-login')


def user_info(request: HttpRequest) -> HttpResponse:
    r = requests.get('https://api.github.com/user', headers={
        'Authorization': 'token %s' % request.session["GITHUB_TOKEN"],
        'Accept': 'application/vnd.github.v3+json'
    })
    return JsonResponse(r.json())


def create_repo(request: HttpRequest, repo_name: str) -> HttpResponse:
    if repo_name == "":
        return redirect('create-repo')
    r = requests.post('https://api.github.com/user/repos',
                      headers={
                          'Authorization': 'token %s' % request.session["GITHUB_TOKEN"],
                          'Accept': 'application/vnd.github.v3+json'
                      },
                      json={
                          'name': repo_name
                      })
    return JsonResponse(r.json())
