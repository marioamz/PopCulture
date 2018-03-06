from django.contrib import admin

# Register your models here.
from .models import Event, Media, TopSents, CompoundSents

admin.site.register(Media)
admin.site.register(Event)
admin.site.register(TopSents)
admin.site.register(CompoundSents)
