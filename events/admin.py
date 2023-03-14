from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('worker', 'client', 'date', 'start_time')

admin.site.register(Event, EventAdmin)
