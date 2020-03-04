from tastypie.resources import ModelResource
from mercury.models import EventCodeAccess, TemperatureSensor


class EventResource(ModelResource):
    class Meta:
        queryset = EventCodeAccess.objects.all()
        resource_name = "events"
        list_allowed_methods = ["get", "post"]
        detail_allowed_methods = ["get", "put", "delete"]


class SensorResource(ModelResource):
    class Meta:
        queryset = TemperatureSensor.objects.all()
        resource_name = "sensor"
