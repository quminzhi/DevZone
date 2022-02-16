from django.contrib import admin
from .models import Profile, Skill, Message, User

# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)