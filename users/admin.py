from django.contrib import admin

from .models import Heart, Message, Profile

# Register your models here.


admin.site.register(Profile)
admin.site.register(Heart)
admin.site.register(Message)
