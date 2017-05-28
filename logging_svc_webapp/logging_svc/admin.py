from django.contrib import admin
from .models import Task, Play, Event, LogFile

admin.site.register(Task)
admin.site.register(Play)
admin.site.register(Event)
admin.site.register(LogFile)
