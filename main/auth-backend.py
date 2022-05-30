from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from main.models import GitHubUser


class GithubBackend(BaseBackend):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, username=None, auth_token=None):
        pwd_valid = auth_token != ""
        if pwd_valid:
            try:
                user = GitHubUser.objects.get(username=username)
            except GitHubUser.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = GitHubUser(username=username, token=auth_token)
                user.is_staff = False
                user.is_superuser = False
                user.save()
            except Exception as e:
                raise (Exception("foobaar"+e.__str__()))
            return user
        return None

    def get_user(self, user_id):
        try:
            return GitHubUser.objects.get(pk=user_id)
        except GitHubUser.DoesNotExist:
            return None
