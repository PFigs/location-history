from ..timeline import Timeline
from ..event import Event
from ..error import DateEndError
from typing import Any

import ijson
import datetime


class TakeoutEvent(Event):
    """TakeoutEvent"""

    def __init__(self, kwargs):

        super(TakeoutEvent, self).__init__(
            date=kwargs["date"],
            latitude=kwargs["latitude"],
            longitude=kwargs["longitude"],
            altitude=kwargs["altitude"],
        )

        self.accuracy = kwargs["accuracy"]


class Takeout(Timeline):
    """Takeout"""

    SEARCHING = 1
    START_EVENT = 2
    END_EVENT = 3

    def __init__(self, filepath: str):
        super(Takeout, self).__init__()

        self.filepath = filepath
        self._fd = None
        self._parse = None
        self.info = None
        self.events = dict()
        self.load()

    def load(self):
        if self._fd:
            self._fd.close()
        self._fd = open(self.filepath, "r")
        self._parser = ijson.parse(self._fd)

    def add(self, **kwargs):

        key = kwargs["date"].isoformat()
        event = TakeoutEvent(kwargs)
        self.events[key] = event

    def item_start(self, prefix: str, event: str, value: Any, storage: dict = None):

        if prefix == "locations.item" and event == "start_map":
            return True
        else:
            return False

    def item_end(self, prefix: str, event: str, value: Any, storage: dict = None):

        if prefix == "locations.item" and event == "end_map":
            return True

        return False

    def item_acquire(
        self,
        prefix: str,
        event: str,
        value: Any,
        storage: dict,
        start: datetime.datetime = None,
        end: datetime.datetime = None,
    ):

        if prefix == "locations.item.timestampMs":
            date = float(value.encode()) / 1e3
            date = datetime.datetime.fromtimestamp(date)

            # check if time is legal
            if start is not None:
                if date < start:
                    return False
            if end is not None:
                if date > end:
                    raise DateEndError

            storage["date"] = date

        if prefix == "locations.item.latitudeE7":
            storage["latitude"] = value * 1e-7

        elif prefix == "locations.item.longitudeE7":
            storage["longitude"] = value * 1e-7

        elif prefix == "locations.item.altitude":
            storage["altitude"] = value

        elif prefix == "locations.item.accuracy":
            storage["accuracy"] = value

        elif prefix in "locations.item.activity":
            pass

        return True

    def browse(self, start=None):

        prefixes = set()
        events = set()
        info = dict(start=None, end=None, nb_entries=0)

        for prefix, event, value in self._parser:
            prefixes.add(prefix)
            events.add(event)

            if self.item_start(prefix, event, value):
                info["nb_entries"] = info["nb_entries"] + 1

            if prefix == "locations.item.timestampMs":
                timestamp = float(value.encode()) / 1e3
                date = datetime.datetime.fromtimestamp(timestamp)
                if info["start"] is None:
                    info["start"] = date
                    info["start_timestamp"] = timestamp
                info["end"] = date
                info["end_timestamp"] = timestamp

        self.info = info

        return info

    def lookup(self, start: datetime.datetime = None, end: datetime.datetime = None):

        storage = dict()
        self.state = self.SEARCHING

        for prefix, event, value in self._parser:

            if self.state == self.SEARCHING:
                if self.item_start(prefix, event, value, storage):
                    self.state = self.START_EVENT
                    storage.clear()
                continue

            if self.state == self.START_EVENT:

                if self.item_end(prefix, event, value, storage):
                    self.add(**storage)
                    self.state = self.SEARCHING
                    continue

                try:
                    if self.item_acquire(prefix, event, value, storage, start, end):
                        continue
                    else:
                        self.state = self.SEARCHING
                except DateEndError:
                    break
