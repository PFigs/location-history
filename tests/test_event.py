import timemap
import datetime


class Defaults(object):
    latitude = 1
    longitude = 1
    altitude = 0


def create_event(date=None, latitude=None, longitude=None, altitude=None):

    if date is None:
        date = datetime.datetime.now()

    if latitude is None:
        latitude = Defaults.latitude

    if longitude is None:
        longitude = Defaults.longitude

    if altitude is None:
        altitude = Defaults.altitude

    event = timemap.Event(
        date=date, latitude=latitude, longitude=latitude, altitude=altitude
    )

    return event


def test_creation():

    event = create_event()

    dlat = abs(Defaults.latitude - event.latitude)
    dlon = abs(Defaults.longitude - event.longitude)
    assert dlat < 1e-6
    assert dlon < 1e-6


def test_serialization():
    event = create_event()
    print(str(event))
