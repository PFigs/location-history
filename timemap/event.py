from .utils import DateTimeEncoder
import datetime
import geopy
import json


class Event(object):
    """
    Event

    Interface definition for a timeline occurance


    """

    def __init__(
        self,
        date: datetime.datetime,
        latitude: float,
        longitude: float,
        altitude: float = 0,
    ):
        super(Event, self).__init__()

        self.date = date
        self.lla = geopy.point.Point(latitude, longitude, altitude)
        self.distance = None

    def distance_to(self, latitude, longitude, altitude):

        _reference_point = [latitude, longitude, altitude]
        self.distance = geopy.distance.geodesic(self.lla, _reference_point)

    def __str__(self):
        """String representation of object"""
        return json.dumps(self.__dict__, cls=DateTimeEncoder)
