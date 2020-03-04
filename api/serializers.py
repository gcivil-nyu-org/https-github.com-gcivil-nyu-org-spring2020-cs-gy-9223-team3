from rest_framework import serializers
from .models import AGEvent
import uuid


class AGEventSerializer(serializers.ModelSerializer):
    agEventID = serializers.UUIDField(
        source="event_uuid", read_only=True, default=uuid.uuid4
    )
    agEventName = serializers.CharField(source="event_name")
    agEventDate = serializers.DateTimeField(source="event_date")
    agEventDescription = serializers.CharField(source="event_description")

    class Meta:
        model = AGEvent
        fields = ["agEventID", "agEventName", "agEventDate", "agEventDescription"]
