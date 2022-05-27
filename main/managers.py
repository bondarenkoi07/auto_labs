from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from main.models import User


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    model = User

    def create_user(self, username, token, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username or not token:
            raise ValueError(_("The Email must be set"))
        user = self.model(username, **extra_fields)
        user.token = token
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
