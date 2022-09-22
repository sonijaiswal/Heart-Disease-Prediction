from django.contrib import admin

from .models import Heart, Message, Profile

# Register your models here.


admin.site.register(Profile)
# admin.site.register(Heart)

admin.site.register(Message)


@admin.register(Heart)
class HeartAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "result1",
        "result2",
        "result3",
    )
