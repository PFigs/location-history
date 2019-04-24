import timemap
import datetime

gmaps_sample = "./tests/gmaps_sample.json"
FILE_START = "2018-04-19T21:07:52.746000"
FILE_END = "2018-04-19T20:47:20.433000"


def test_json_browse():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()


def test_accuracy_set():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.lookup()
    for day, events in takeout:
        for event in events.values():
            print(event)

    assert event.accuracy > 0


def test_json_lookup():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()
    takeout.load()
    takeout.lookup()
    assert len(takeout) == takeout.report["nb_entries"]
    assert len(takeout) > 0

    return takeout


def test_json_lookup_with_start():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()
    start = datetime.datetime.fromtimestamp(takeout.report["start_timestamp"])
    takeout.load()
    takeout.lookup(start=start)
    assert len(takeout) == takeout.report["nb_entries"]
    assert len(takeout) > 0


def test_json_lookup_with_start_end():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()
    start = datetime.datetime.fromtimestamp(takeout.report["start_timestamp"])
    end = datetime.datetime.fromtimestamp(takeout.report["end_timestamp"])

    takeout.load()
    takeout.lookup(start=start, end=end)
    assert len(takeout) > 0

    assert len(takeout) == takeout.report["nb_entries"]


def test_json_lookup_with_end():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()
    end = datetime.datetime.fromtimestamp(takeout.report["end_timestamp"])

    takeout.load()
    takeout.lookup(end=end)

    assert len(takeout) == takeout.report["nb_entries"]


def test_event_filter_none():
    def event_filter(event, latitude, longitude, altitude, radius, **kwargs):
        event.distance_3d(latitude, longitude, altitude)
        if event.distance > radius:
            return False
        return True

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    args = dict(latitude=0, longitude=0, altitude=0, radius=10)
    takeout.lookup(event_filter=event_filter, event_filter_args=args)
    takeout.summary()
    assert len(takeout) == 0
    assert takeout.report["nb_entries"] == 0


def test_event_filter_some():
    def event_filter(event, latitude, longitude, altitude, radius, **kwargs):
        event.distance_2d(latitude, longitude, altitude)
        if event.distance > radius:
            return False
        return True

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    args = dict(latitude=0, longitude=0, altitude=0, radius=10230370)
    takeout.lookup(event_filter=event_filter, event_filter_args=args)
    assert len(takeout) > 0
    assert takeout.report["nb_entries"] > 0


def test_daily_report():
    def event_filter(event, latitude, longitude, altitude, radius, **kwargs):
        event.distance_2d(latitude, longitude, altitude)
        if event.distance > radius:
            return False
        return True

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    args = dict(latitude=0, longitude=0, altitude=0, radius=10230370)
    takeout.lookup(event_filter=event_filter, event_filter_args=args)

    takeout.report.total_daily(takeout.events)
    for item in takeout.report.daily:
        item.describe()
    takeout.summary()

    takeout.report.total_monthly()
    for item in takeout.report.montlhy:
        item.describe()
    takeout.summary(monthly=True)


if __name__ == "__main__":
    takeout = test_json_lookup()
