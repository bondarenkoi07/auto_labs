from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import GitHubUser

admin.site.register(GitHubUser, UserAdmin)
