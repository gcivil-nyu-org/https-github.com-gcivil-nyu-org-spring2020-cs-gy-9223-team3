from django.db import models
import uuid
from django.utils import timezone


class AGEvent(models.Model):
    """This model stores the information about events. When a new event is created,
    a UUID4-typed event_uuid will be assigned to this event and also store the current
    date for this event. """

    event_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=40, blank=True)
    event_date = models.DateTimeField(default=timezone.now)
    event_description = models.CharField(max_length=100, null=True, blank=True)
