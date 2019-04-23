import json
import datetime
import geopy


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, (datetime.date, datetime.datetime)):
            obj = obj.isoformat()
            return obj

        if isinstance(obj, (geopy.Point)):
            return str([obj.latitude, obj.longitude, obj.altitude])

        return json.JSONEncoder.default(self, obj)
