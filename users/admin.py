from django.contrib import admin

# Register your models here.

from .models import Profile, Message,Heart

admin.site.register(Profile)
admin.site.register(Heart)
admin.site.register(Message)
