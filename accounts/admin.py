from django.contrib import admin
from django.contrib.auth.models import User

from accounts.models import Profile

admin.site.register(Profile)

