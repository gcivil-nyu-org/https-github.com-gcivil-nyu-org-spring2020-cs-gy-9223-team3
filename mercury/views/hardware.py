import logging
import glob
import serial
import asyncio
import serial_asyncio

from django.utils import dateparse
from django.views.generic import TemplateView
from django.http import HttpResponse

from mercury.event_check import require_event_code
from mercury.models import GeneralData, Events, Field, Sensor

log = logging.getLogger(__name__)


class HardwareView(TemplateView):
    @require_event_code
    def get(self, request, *args, **kwargs):
        """The get request sent from web to determine the parameters of the serial port
            Url Sample:
            https://localhost:8000/hardware?enable=1&baudrate=8000&bytesize=8
                &parity=N&stopbits=1&timeout=None

                enable: must define, set the port on if 1, off if 0
                baudrate: Optional, default 9600
                bytesize: Optional, default 8 bits
                parity: Optional, default no parity
                stop bits: Optional, default one stop bit
                timeout: Optional, default 1 second
            """
        enable = request.GET.get("enable")
        if enable is None:
            return

        ser = serial.Serial()
        ports = glob.glob("/dev/tty.*")
        ser.port = ports[0]
        if enable == "1":
            if request.GET.get("baudrate"):
                ser.baudrate = request.GET.get("baudrate")
            if request.GET.get("bytesize"):
                ser.bytesize = request.GET.get("bytesize")
            if request.GET.get("parity"):
                ser.parity = request.GET.get("parity")
            if request.GET.get("stopbits"):
                ser.stopbits = request.GET.get("stopbits")
            if request.GET.get("timeout"):
                ser.timeout = request.GET.get("timeout")
            ser.open()

            loop = asyncio.new_event_loop()
            coro = serial_asyncio.create_serial_connection(loop, AsyncSerialProtocol, ports[0])
            try:
                loop.run_until_complete(coro)
                loop.run_forever()
            finally:
                loop.close()
        else:
            if ser.is_open:
                ser.close()
            log.info("Serial port is close")

        return HttpResponse(status=201)

    def json_to_models(self, json_str, event_id):
        """
        Json example:
        {
        sensors:{
            ss_id : “Sensor id”,
            ss_value : {
                /*as many values as you wish*/
                value_a_name : “value_a”,
                value_b_name : “value_b”,
                value_c_name : “value_c”
            }
            date : “2014-03-12T13:37:27+00:00” /*ISO 8601 dates*/
        }
        """
        res = []
        sensors = json_str["sensors"]
        ss_id = int(sensors["ss_id"])
        ss_value = sensors["ss_value"]
        date = dateparse.parse_datetime(sensors["date"])

        for i, f in enumerate( ss_value):
            field_id = int(f)
            data_value = float(ss_value[f])
            event = Events.objects.get(event_id=event_id)
            field = Field.objects.get(field_id=field_id)
            sensor = Sensor.objects.get(sensor_id=ss_id)

            general_data = GeneralData(
                sensor_id=sensor,
                stored_at_time=date,
                event_id=event,
                field_id=field,
                data_value=data_value,
            )
            res.append(general_data)

        return res


class AsyncSerialProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False
        transport.write(b'hello world\n')

    def data_received(self, data):
        print('data received', repr(data))
        models = HardwareView.json_to_models(repr(data))
        for m in models:
            m.save()
        self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()
