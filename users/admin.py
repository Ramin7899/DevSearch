from django.contrib import admin

# Register your models here.

from .models import Profiles, Skills, Message

admin.site.register(Profiles)
admin.site.register(Skills)
admin.site.register(Message)
