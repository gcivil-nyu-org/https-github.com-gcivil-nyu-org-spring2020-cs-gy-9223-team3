from api.models import AGEvent
from api.serializers import AGEventSerializer

from rest_framework import generics


class EventList(generics.ListCreateAPIView):
    """
    List all events, or create a new event.
    
    get:
    Return a list of all the existing events.

    post:
    Create a new event, whose UUID will be specified by the system.
    """

    queryset = AGEvent.objects.all()
    serializer_class = AGEventSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an event.

    get:
    Return a specific event.

    put:
    Update an event with its UUID.

    delete:
    Delete an event with its UUID.
    """

    queryset = AGEvent.objects.all()
    serializer_class = AGEventSerializer
