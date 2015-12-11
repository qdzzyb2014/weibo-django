from django.contrib import admin

# Register your models here.
from main.models import User, Role

admin.site.register(User)
admin.site.register(Role)