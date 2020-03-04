from api.models import AGEvent
from api.serializers import AGEventSerializer

from rest_framework import generics


class EventList(generics.ListCreateAPIView):
    """
    List all events, or create a new event.
    """

    queryset = AGEvent.objects.all()
    serializer_class = AGEventSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an event.
    """

    queryset = AGEvent.objects.all()
    serializer_class = AGEventSerializer
