from django.contrib import admin
from .models import User, Client, Worker, Schedule

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'username', 'email')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('worker', 'start_time', 'end_time')


admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Schedule, ScheduleAdmin)
