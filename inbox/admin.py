from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'receiver', 'timestamp')


admin.site.register(Notification, NotificationAdmin)
