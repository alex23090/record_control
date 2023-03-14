from django.db import models
from events.models import Event
from core.models import User
import uuid


class Notification(models.Model):
    content = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False, null=True)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note_initiator")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note_receiver")
    timestamp = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.initiator.first_name) + " - " + str(self.receiver.first_name) + " " + str(self.timestamp)
