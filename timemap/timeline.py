import datetime


class Timeline(object):
    """
    Timeline

    This class defines what events and with which order they have happened over
    a period of time.

    """

    def __init__(self):
        super(Timeline, self).__init__()
        self.events = None  # source it
        self.report = None  # Report()

    def lookup(self, start: datetime.datetime, end: datetime.datetime):
        raise NotImplementedError

    def map_distance(self, reference: list[float]):
        """
        Computes distance to a reference point reference point
        """
        return list(map(lambda x: x.distance_to(self.events), self.events))

    def filter_by_radius(self, radius: float):
        """
        Filter out events outside validity radius
        """
        return list(filter(lambda x: x.distance.meters < radius, self.events))

    # allow for attribute indexing
    def __getitem__(self, key):
        """ Loops through inpection on for loops """
        return self.events[key]
