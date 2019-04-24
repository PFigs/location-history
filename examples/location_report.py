import timemap
import datetime


def event_filter(event, latitude, longitude, radius, **kwargs):
    event.distance_2d(latitude, longitude)
    if event.distance < float(radius):
        return True
    return False


if __name__ == "__main__":
    settings = timemap.ParserHelper.default_args().settings(skip_undefined=True)
    takeout = timemap.gmaps.Takeout(filepath=settings.filepath)
    takeout.lookup(
        start=datetime.datetime.fromordinal(settings.start.toordinal()),
        end=datetime.datetime.fromordinal(settings.end.toordinal()),
        event_filter=event_filter,
        event_filter_args=settings.__dict__,
    )
    report = takeout.summary(monthly=True)
    report = takeout.summary()
