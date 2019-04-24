from .utils import DateTimeEncoder
import json


class Report(object):
    """Report"""

    def __init__(self):
        super(Report, self).__init__()
        self.start = None
        self.end = None
        self.nb_entries = 0
        self.start_timestamp = None
        self.end_timestamp = None

    def clear(self):
        self.start = None
        self.end = None
        self.nb_entries = 0
        self.start_timestamp = None
        self.end_timestamp = None

    def add(self, date, descending=True):

        self.nb_entries = self.nb_entries + 1

        if descending:
            if self.end is None:
                self.end = date
                self.end_timestamp = date.timestamp()
            else:
                self.start = date
                self.start_timestamp = date.timestamp()
        else:
            if self.start is None:
                self.start = date
                self.end_timestamp = date.timestamp()
            else:
                self.end = date
                self.end_timestamp = date.timestamp()

    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self) -> str:
        """String representation of object"""
        return json.dumps(self.__dict__, cls=DateTimeEncoder)
