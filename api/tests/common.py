from api.models import AGEvent

test_event_data = {
    "event1": {
        "agEventName": "Sunny Day Test Drive",
        "agEventDate": "2020-02-02T20:21:22",
        "agEventDescription": "A very progressive test run at \
            Sunnyside Daycare's Butterfly Room.",
    },
    "event2": {
        "agEventName": "Peppa Pig Muddy Puddles",
        "agEventDate": "2020-03-01T00:34:57",
        "agEventDescription": "George, \
            if you jump in muddy puddles, you must wear your boots.",
    },
}


def create_event(event):
    return AGEvent(
        event_name=event["agEventName"],
        event_date=event["agEventDate"],
        event_description=event["agEventDescription"],
    )
