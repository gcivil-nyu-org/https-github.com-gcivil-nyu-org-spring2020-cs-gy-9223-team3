from rest_framework.test import APITestCase, URLPatternsTestCase
from django.test import TestCase
from django.utils.dateparse import parse_datetime
from api.tests import common
from api.serializers import AGEventSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io
from django.urls import include, path, reverse
from api.models import AGEvent
import uuid


class AGEventAPISerializationTest(TestCase):
    def test_event_serialization(self):
        # prepare an event object
        agEvent = common.create_event(common.test_event_data["event1"])
        # serialize data
        serializer = AGEventSerializer(agEvent)
        self.assertEqual(serializer.instance.event_name, agEvent.event_name)
        self.assertEqual(serializer.instance.event_date, agEvent.event_date)
        self.assertEqual(
            serializer.instance.event_description, agEvent.event_description
        )
        # render to json
        jsonContent = JSONRenderer().render(serializer.data)
        # deserialize: parse the stream to python native
        stream = io.BytesIO(jsonContent)
        parsedData = JSONParser().parse(stream)
        self.assertEqual(parsedData["agEventName"], agEvent.event_name)
        self.assertEqual(parsedData["agEventDate"], agEvent.event_date)
        self.assertEqual(parsedData["agEventDescription"], agEvent.event_description)
        # deserialize: populate object instance
        serializer = AGEventSerializer(data=parsedData)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["event_name"], agEvent.event_name)
        self.assertEqual(
            serializer.validated_data["event_date"], parse_datetime(agEvent.event_date)
        )
        self.assertEqual(
            serializer.validated_data["event_description"], agEvent.event_description
        )


class AGEventListAPITest(APITestCase, URLPatternsTestCase):

    urlpatterns = [path("api/v1/", include("api.urls"), name="api")]

    def test_event_list_get_empty(self):
        url = reverse("api:event-list")
        # Check empty list
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_event_list_get_nonempty(self):
        url = reverse("api:event-list")
        # Check list with single event
        agEvent1 = common.create_event(common.test_event_data["event1"])
        agEvent1.event_uuid = uuid.uuid4()
        agEvent1.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["agEventID"], str(agEvent1.event_uuid))
        self.assertEqual(response.data[0]["agEventName"], str(agEvent1.event_name))
        self.assertEqual(response.data[0]["agEventDate"], str(agEvent1.event_date))
        self.assertEqual(
            response.data[0]["agEventDescription"], str(agEvent1.event_description)
        )
        # Check list with multiple events
        agEvent2 = common.create_event(common.test_event_data["event2"])
        agEvent2.event_uuid = uuid.uuid4()
        agEvent2.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["agEventID"], str(agEvent1.event_uuid))
        self.assertEqual(response.data[0]["agEventName"], str(agEvent1.event_name))
        self.assertEqual(response.data[0]["agEventDate"], str(agEvent1.event_date))
        self.assertEqual(
            response.data[0]["agEventDescription"], str(agEvent1.event_description)
        )
        self.assertEqual(response.data[1]["agEventID"], str(agEvent2.event_uuid))
        self.assertEqual(response.data[1]["agEventName"], str(agEvent2.event_name))
        self.assertEqual(response.data[1]["agEventDate"], str(agEvent2.event_date))
        self.assertEqual(
            response.data[1]["agEventDescription"], str(agEvent2.event_description)
        )

    def test_event_list_post_create_event(self):
        url = reverse("api:event-list")
        # Create an event in empty list
        agEventData = common.test_event_data["event1"]
        response = self.client.post(url, agEventData)
        self.assertEqual(response.status_code, 201)
        agEventInDB = AGEvent.objects.all()
        self.assertEqual(agEventInDB.count(), 1)
        agEventInDB = agEventInDB.first()
        self.assertEqual(response.data["agEventID"], str(agEventInDB.event_uuid))
        self.assertEqual(response.data["agEventName"], str(agEventInDB.event_name))
        self.assertEqual(
            parse_datetime(response.data["agEventDate"]), agEventInDB.event_date
        )
        self.assertEqual(
            response.data["agEventDescription"], str(agEventInDB.event_description)
        )
        # Create an event in nonempty list
        agEventData = common.test_event_data["event1"]
        response = self.client.post(url, agEventData)
        self.assertEqual(response.status_code, 201)
        agEventInDB = AGEvent.objects.all()
        self.assertEqual(agEventInDB.count(), 2)
        agEventInDB = agEventInDB[1]
        self.assertEqual(response.data["agEventID"], str(agEventInDB.event_uuid))
        self.assertEqual(response.data["agEventName"], str(agEventInDB.event_name))
        self.assertEqual(
            parse_datetime(response.data["agEventDate"]), agEventInDB.event_date
        )
        self.assertEqual(
            response.data["agEventDescription"], str(agEventInDB.event_description)
        )
        # Create an event in nonempty list
        agEventData = common.test_event_data["event2"]
        response = self.client.post(url, agEventData)
        self.assertEqual(response.status_code, 201)
        agEventInDB = AGEvent.objects.all()
        self.assertEqual(agEventInDB.count(), 3)
        agEventInDB = agEventInDB[2]
        self.assertEqual(response.data["agEventID"], str(agEventInDB.event_uuid))
        self.assertEqual(response.data["agEventName"], str(agEventInDB.event_name))
        self.assertEqual(
            parse_datetime(response.data["agEventDate"]), agEventInDB.event_date
        )
        self.assertEqual(
            response.data["agEventDescription"], str(agEventInDB.event_description)
        )

    def test_event_list_other_methods(self):
        url = reverse("api:event-list")
        response = self.client.head(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.options(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.put(url)
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 405)
        response = self.client.trace(url)
        self.assertEqual(response.status_code, 405)
