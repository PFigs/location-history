from .utils import DateTimeEncoder
import datetime
import json
from .event import Event
from .report import Report
from typing import List, Union, Callable


class Timeline(object):
    """
    Timeline

    This class defines what events and with which order they have happened over
    a period of time.

    """

    def __init__(self) -> "Timeline":
        super(Timeline, self).__init__()
        self.events = dict()
        self.report = Report()

    def add(
        self, event_filter: Callable = None, event_filter_args: dict = None, **kwargs
    ) -> Union[Event, None]:

        is_valid = True
        key = kwargs["date"].isoformat()
        event = Event(
            date=kwargs["date"],
            latitude=kwargs["latitude"],
            longitude=kwargs["longitude"],
            altitude=kwargs["altitude"],
        )

        if event_filter is not None:

            if event_filter_args is None:
                event_filter_args = dict()

            is_valid = event_filter(event, **event_filter_args)

        if is_valid is True:
            self.report.add(event.date)
            self.events[key] = event
            return event

    def lookup(
        self,
        start: datetime.datetime,
        end: datetime.datetime,
        event_filter: Callable = None,
        event_filter_args: dict = None,
    ) -> None:
        """
        Method to be implemented in specialized class
        """
        raise NotImplementedError

    def map_distance(self, reference: List[float]) -> List[Event]:
        """
        Computes distance to a reference point reference point
        """
        return list(map(lambda x: x.distance_to(self.events), self.events))

    def filter_by_radius(self, radius: float) -> List[Event]:
        """
        Filter out events outside validity radius
        """
        return list(filter(lambda x: x.distance.meters < radius, self.events))

    def summary(self) -> dict:
        """ Loops throw the events and updates the report summary """
        self.report.clear()
        for _, event in self.events.items():
            self.report.count()
            self.report.add(event.date)
            print(
                "{}@[{},{},{}]".format(
                    event.date, event.latitude, event.longitude, event.longitude
                )
            )
        return self.report

    def __getitem__(self, key) -> Event:
        return self.events[key]

    def __iter__(self) -> Event:
        for event in self.events.items():
            yield event

    def __len__(self) -> int:
        return len(self.events)

    def __str__(self) -> str:
        return str(self.events)
