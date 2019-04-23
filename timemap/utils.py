import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        obj["time"] = obj["time"].isoformat()
        return json.JSONEncoder.default(self, obj)
