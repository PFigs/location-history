import datetime
from .event import Event
from typing import List


class Timeline(object):
    """
    Timeline

    This class defines what events and with which order they have happened over
    a period of time.

    """

    def __init__(self):
        super(Timeline, self).__init__()
        self.events = dict()
        self.report = None  # Report()

    def add(self, **kwargs):

        key = kwargs["date"].isoformat()
        event = Event(
            date=kwargs["date"],
            latitude=kwargs["latitude"],
            longitude=kwargs["longitude"],
            altitude=kwargs["altitude"],
        )
        self.events[key] = event

    def lookup(self, start: datetime.datetime, end: datetime.datetime):
        raise NotImplementedError

    def map_distance(self, reference: List[float]):
        """
        Computes distance to a reference point reference point
        """
        return list(map(lambda x: x.distance_to(self.events), self.events))

    def filter_by_radius(self, radius: float):
        """
        Filter out events outside validity radius
        """
        return list(filter(lambda x: x.distance.meters < radius, self.events))

    def __getitem__(self, key):
        return self.events[key]

    def __iter__(self):
        for event in self.events:
            yield event

    def __len__(self):
        return len(self.events)

    def __str__(self):
        return str(self.events)
