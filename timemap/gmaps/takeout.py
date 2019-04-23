from ..timeline import Timeline
from ..event import Event
import ijson
import datetime


class Takeout(Timeline):
    """docstring for Takeout"""

    def __init__(self, filepath: str):
        super(Takeout, self).__init__()

        self.filepath = filepath
        self._fd = open(self.filepath, "r")
        self._parser = ijson.parse(self._fd)

    def _json_lookup(self, start: datetime.datetime, end: datetime.datetime):
        # updates date list
        numdays = (end - start).days
        self.date_list = [start + datetime.timedelta(days=x) for x in range(0, numdays)]

        # streams in json file and build point based on timestamp,
        # latitude and longitude.
        self.inspection = list()
        complete = False
        for prefix, event, value in self._parser:
            if prefix.endswith(".timestampMs"):
                date = float(value.encode()) / 1000.0
                date = datetime.datetime.fromtimestamp(date)
                complete = False

            elif prefix.endswith(".latitudeE7"):
                latitude = value * 1e-7

            elif prefix.endswith(".longitudeE7"):
                longitude = value * 1e-7
                complete = True
            else:
                continue

            if complete is True:
                complete = False
                if date >= start and date <= end:
                    self.inspection.append(
                        Event(date=date, latitude=latitude, longitude=longitude)
                    )
                    continue

                elif self.inspection:
                    break
