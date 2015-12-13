from django.contrib import admin

# Register your models here.
from main.models import User, Role, Post

'''
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Post)
'''
registe_list = [User, Role, Post]
for i in registe_list:
    admin.site.register(i)
