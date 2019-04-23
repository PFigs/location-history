import math
import timemap


def test_event_creation(latitude=1, longitude=1):

    event = timemap.Event(latitude=latitude, longitude=latitude)
    dlat = math.abs(latitude - event.latitude)
    dlon = math.abs(longitude - event.longitude)
    assert dlat < 1e-6
    assert dlon < 1e-6
