"""
    Report

    This module contains classes that offer a summary of events
    over a span of time.

"""

import datetime
import json
from .utils import DateTimeEncoder


class Breakdown(object):
    """
        Breakdown

        This class is an helper for the Report class.

        A Breakdown object stores for a given date, the
        amount of events and time spent withing the location of
        interest.
    """

    def __init__(self, date: datetime.datetime):
        super(Breakdown, self).__init__()
        self.date = date
        self.seconds = 0
        self.hours = 0
        self.count = 0
        self.previous = None
        self.current = None

    def add(self, date: datetime.datetime, max_interval: int = 1 * 60 * 60):
        """ Adds the event to the daily breakdown """
        self.count += 1
        self.current = date

        if self.previous is not None:
            if self.previous < self.current:
                event_a = self.current
                event_b = self.previous
            else:
                event_a = self.previous
                event_b = self.current

            interval = (event_a - event_b).total_seconds()
            if interval < max_interval:
                self.seconds += interval

        self.hours = self.seconds / (60 * 60)
        self.previous = date

    def describe(self):
        """ Prints information about itself, such as
        which date it refers to and how many events have occured. """
        print("date: {}".format(self.date))
        print("  events: {}".format(self.count))
        print("  hours: {}".format(self.hours))

    def sum(self, other):
        """ Sums two breakdown objects together """
        self.hours += other.hours
        self.seconds += other.seconds
        self.count += 1

    def __str__(self) -> str:
        return json.dumps(self.__dict__, cls=DateTimeEncoder)


class Report(object):
    """
    Report

    This class offers a collection of daily and monthly events
    that have occured over the timespan defined in the start_timestamp
    and end_timestamp properties.

    """

    def __init__(self):
        super(Report, self).__init__()
        self.start = None
        self.end = None
        self.nb_entries = 0
        self.start_timestamp = None
        self.end_timestamp = None
        self._daily = dict()
        self._monthly = dict()

    def clear(self):
        """ Resets the internal variables"""
        self.start = None
        self.end = None
        self.nb_entries = 0
        self.start_timestamp = None
        self.end_timestamp = None
        self._daily = dict()
        self._monthly = dict()

    def add(self, date: datetime.datetime):
        """ Adds an event into the report """
        self.nb_entries = self.nb_entries + 1
        timestamp = date.timestamp()

        if self.end is None and self.start is None:
            self.end = date
            self.end_timestamp = timestamp

            self.start = date
            self.start_timestamp = timestamp

        else:
            if date > self.end:
                self.end = date
                self.end_timestamp = timestamp
            else:
                self.start = date
                self.start_timestamp = timestamp

        key = date.date().isoformat()
        if key not in self._daily:
            self._daily[key] = Breakdown(date)
        self._daily[key].add(date)

    @property
    def daily(self) -> Breakdown:
        """ Yields all the daily breakdown events """
        for _, value in self._daily.items():
            yield value

    @property
    def montlhy(self) -> Breakdown:
        """ Computes the montly breakdown and yields each monthly breakdown """
        self.total_monthly()
        for _, value in self._monthly.items():
            yield value

    def total_daily(self, events: dict):
        """ Computes the daily breakdown for all Report events"""
        self._daily.clear()
        for key, event in events.items():

            if key not in self._daily:
                date = datetime.datetime.strptime(key, "%Y-%m-%d")
                self._daily[key] = Breakdown(date)

            for _, day_event in event.items():
                self._daily[key].add(day_event.date)

        return self._daily

    def total_monthly(self):
        """ Computes the monthly breakdown for all Report events"""
        self._monthly.clear()
        for _, breakdown in self._daily.items():
            date = breakdown.date
            key = "{}{}".format(date.year, date.month)

            if key not in self._monthly:
                self._monthly[key] = Breakdown(date)

            self._monthly[key].sum(breakdown)

        return self._monthly

    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self) -> str:
        return str(self.__dict__)
