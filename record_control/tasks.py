from django_q.tasks import schedule
from events.models import Event
from inbox.models import Notification
import datetime


def auto_delete_events():
    Event.objects.filter(date__lte=datetime.date.today()-datetime.timedelta(days=7), success=True).delete()


def auto_delete_notifications():
    Notification.objects.filter(timestamp__lte=datetime.date.today()-datetime.timedelta(days=7), success=True).delete()


schedule('tasks.auto_delete_events', minutes=1)
schedule('tasks.auto_delete_notifications', minutes=1)
