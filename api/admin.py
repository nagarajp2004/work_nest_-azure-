
from django.contrib import admin

from .models import User, Task, Permission


admin.site.register(User)


admin.site.register(Task)


admin.site.register(Permission)
