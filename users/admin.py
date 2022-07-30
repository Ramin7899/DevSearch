from django.contrib import admin

# Register your models here.

from .models import Profiles, Skills

admin.site.register(Profiles)
admin.site.register(Skills)
