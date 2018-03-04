from django.contrib import admin

# Register your models here.
from .models import Event, Media

admin.site.register(Media)
admin.site.register(Event)
