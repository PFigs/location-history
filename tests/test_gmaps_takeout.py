import timemap
import datetime

gmaps_sample = "./tests/gmaps_sample.json"
FILE_START = "2018-04-19T21:07:52.746000"
FILE_END = "2018-04-19T20:47:20.433000"


def test_json_browse():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()


def test_json_lookup():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()
    takeout.load()
    takeout.lookup()
    assert len(takeout) == takeout.info["nb_entries"]


def test_json_lookup_with_start():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()
    start = datetime.datetime.fromtimestamp(takeout.info["end_timestamp"])
    takeout.load()
    takeout.lookup(start=start)
    assert len(takeout) == takeout.info["nb_entries"]


def test_json_lookup_with_start_end():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()
    start = datetime.datetime.fromtimestamp(takeout.info["end_timestamp"])
    end = datetime.datetime.fromtimestamp(takeout.info["start_timestamp"])

    takeout.load()
    takeout.lookup(start=start, end=end)

    assert len(takeout) == takeout.info["nb_entries"]


def test_json_lookup_with_end():

    takeout = timemap.gmaps.Takeout(filepath=gmaps_sample)
    takeout.browse()
    end = datetime.datetime.fromtimestamp(takeout.info["start_timestamp"])

    takeout.load()
    takeout.lookup(end=end)

    assert len(takeout) == takeout.info["nb_entries"]


if __name__ == "__main__":
    test_json_lookup()
