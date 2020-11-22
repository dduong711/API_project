from django.contrib import admin

from .models import MongoDB, Host


admin.site.register(MongoDB)
admin.site.register(Host)
