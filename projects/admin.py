from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag, Heart
from .models import Project, Review, Tag, Heart

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Heart)
