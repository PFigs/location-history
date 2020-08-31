"""
    Timemap

    This file contains the packages' entrypoints.
"""

import datetime

from .utils import ParserHelper
from . import gmaps


def event_filter(event, latitude, longitude, radius, **kwargs):
    """ rule on how to filter the event """
    event.distance_2d(latitude, longitude)

    if event.distance:
        if event.distance < float(radius):
            return True
    return False


def location_report():
    """ entrypoint to calculate a monthly report """

    settings = ParserHelper.default_args().settings(skip_undefined=True)
    takeout = gmaps.Takeout(filepath=settings.filepath)
    takeout.lookup(
        start=datetime.datetime.fromordinal(settings.start.toordinal()),
        end=datetime.datetime.fromordinal(settings.end.toordinal()),
        event_filter=event_filter,
        event_filter_args=settings.__dict__,
    )

    takeout.report.total_monthly()
    for item in takeout.report.montlhy:
        item.describe()
    takeout.summary(monthly=True)


if __name__ == "__main__":
    location_report()
