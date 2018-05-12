# Location History Parser
#
#   This is a parser for gmaps
#   location history in the JSON
#   format provided by Google Takeout
#   as of 09.2017
#
#   Author
#   Pedro Silva
#
#   License
#   MIT

import argparse
import configparser

import copy
import json
import ijson

import datetime

from geopy.point import Point
from geopy.distance import vincenty
from geopy.geocoders import Nominatim


class DateTimeEncoder(json.JSONEncoder):
    
    def default(self, obj):
        print(obj)
        obj['time'] = obj['time'].isoformat()        
        print(obj)

        return json.JSONEncoder.default(self, obj)

class LocationPoint(object):
    """
    Location History point

    This class represents a point in GMAPS location history

    Attributes:
        latitude (#) : latitude in WGS84
        longitude (#) : longitude in WGS84
        timestamp (time) : datetime timestamp
        distance (#) : km to a given reference point

    """

    def __init__(self, latitude, longitude, time):
        """
        Initialises Location Point

        lla (obj) : Geopy's point
        time (datetime) : date in a datetime format
        distance (obj) : Geopy's distance

        """
        super(LocationPoint, self).__init__()
        self.lla = Point(latitude, longitude)
        self.time = time
        self.distance = None

    def distance_to(self, reference_point):
        """
        Calculates distance to REFERENCE_POINT

        Relies on Geopy's Vicenty and stores result
        inside object's attribute distance.

        Note that this is unit agnostic, thus you
        can control the value by selecting:

        - self.distance.km for km

        - self.distance.meters for meters

        """
        self.distance = vincenty(self.lla, reference_point)

    def __str__(self):
        """String representation of object"""
        return str({'lat': self.lla.latitude,
                    'lng': self.lla.longitude,
                    'distance': self.distance,
                    'time': self.time.isoformat()})

    def __repr__(self):
        """How object is interpreted"""
        return self.__str__()


class LocationHistory(object):
    """
        LocationHistory

        This class handles GMAPS location history in a
        JSON format

        It relies on a streaming json package to avoid
        trashing the computer's RAM.

        Attributes:
            filepath (str) : location history disk location
            _fd (int) : file descriptor
            _parser (obj) : ijson parser

            report (dict) : dictionary with dates as keys
            date_list ([]) : array with dates being looked at
            inspection ([]) : period extracted from Location History

    """

    def __init__(self, filepath):
        """
        Constructs a Location History object

        Prepares target for future reading
        """
        super(LocationHistory, self).__init__()

        self.filepath = filepath
        self._fd = open(self.filepath, 'r')
        self._parser = ijson.parse(self._fd)

        self.report = {}
        self.date_list = list()
        self.inspection = list()

    def inspect_date(self, start, end):
        """
        Inpects a date period

        Takes dates in start and end and extracts events between these days
        creating an array of Location Points

        Args:
            start (datetime) : oldest date to look for
            end (datetime) : earliest date to look for

        Returns:
            self.inspection ([]) : array with valid events

        Note, most recent events appear first in the arrays (lowest index)

        """

        # updates date list
        numdays = (end - start).days
        self.date_list = [start + datetime.timedelta(days=x)
                          for x in range(0, numdays)]

        # streams in json file and build point based on timestamp,
        # latitude and longitude.
        self.inspection = list()
        complete = False
        for prefix, event, value in self._parser:
            if prefix.endswith('.timestampMs'):
                time = float(value.encode())/1000.0
                time = datetime.datetime.fromtimestamp(time)
                complete = False

            elif prefix.endswith('.latitudeE7'):
                latitude = value*1e-7

            elif prefix.endswith('.longitudeE7'):
                longitude = value*1e-7
                complete = True
            else:
                continue

            if complete is True:
                complete = False
                if time >= start and time <= end:
                    self.inspection.append(LocationPoint(latitude,
                                                         longitude,
                                                         time))
                    continue

                elif self.inspection:
                    break

    def inspect_distance(self, lla):
        """
        Computes distance to reference point

        Updates geopoints with distance to reference point

        Args:
            lla ([]) : array with decimal latitude and longitude

        """
        if self.inspection:
            self.inpection = list(map(lambda x: x.distance_to(lla), self.inspection))

    def filter_by_radius(self, radius):
        """
        Filter out events outside validity radius

        Args:
            radius (float) : maximum acceptable distance from centre (in meters)

        """
        if self.inspection:
            self.inspection = list(filter(lambda x: x.distance.meters < radius,
                                          self.inspection))

    def build_report(self, start, end, continuous=1*60*60):

        self.report = {}
        if self.inspection:

            # sort out days
            for date in self.date_list:

                day = list(filter(lambda x: (x.time.date() -
                                             date.date()).days == 0,
                                  self.inspection))

                key = date.strftime('%Y-%m-%d')
                if key not in self.report and day:
                    total = 0
                    pevent = day[0]
                    for event in day:

                        elapsed_seconds = (pevent.time
                                           - event.time).total_seconds()
                        if elapsed_seconds < continuous:
                            total = total + elapsed_seconds
                        pevent = event

                    self.report[key] = {'events': day,
                                        'totals': {
                                            'hours': total/(60*60),
                                            'minutes': total/60,
                                            'seconds': total
                                        }
                                        }
                else:
                    continue

    def breakdown(self):
        """ Prints to stdout a summary of hours """

        print('')
        print('breakdown')
        self.range_total = 0
        for key, value in self.report.items():
            print('{0}: {1}h'.format(key, value['totals']['hours']))
            self.range_total = self.range_total + value['totals']['hours']

        print('-------')
        print('mean per day: {0}h'.format(self.range_total/len(self.report)))
        print('total over period: {0}h'.format(self.range_total))


    def write(self, wtype='json'):
        """ 
        Writes the breakdown report to a given target

        Args:
            type (str) : where to write the output

        """

        if wtype == 'json':

            with open('report.json', 'w') as fp:
                output = {
                          'report': str(self.report), 
                          'total': self.range_total,
                          'mean': self.range_total/len(self.report)
                          }

                fp.write(json.dumps(output, cls=DateTimeEncoder))

        else:
            pass


    def __getitem__(self, key):
        """ Loops through inpection on for loops """
        return self.inspection[key]


def parse_args():
    """
    Sets options for command line argumens

    Returns:
        args: list with parsed arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--configuration',
                        default='defaults.ini',
                        type=str)

    parser.add_argument("--filepath", type=str,
                        help="filepath")

    parser.add_argument("--start", type=str,
                        help="start date as YYYY-MM-DD")

    parser.add_argument("--end", type=str,
                        help="end date as YYYY-MM-DD")

    parser.add_argument("--radius", type=float,
                        help="radius (km)")

    parser.add_argument("--latitude", type=float,
                        help="decimal latitude for location report")

    parser.add_argument("--longitude", type=float,
                        help="decimal longitude for location report")

    parser.add_argument("--breaks", type=float,
                        help="maximum time to allow between \
                              two sequential events")

    return parser.parse_args()


def main():

    # reads necessary details
    config = configparser.ConfigParser()
    args = parse_args()
    config.read(args.configuration)

    # evaluates precedence
    if config.has_section('DATE'):

        if args.start is None:
            report_start = config.get('DATE', 'START')
        else:
            report_start = args.start
        report_start = datetime.datetime.strptime(report_start, '%Y-%m-%d')

        if args.end is None:
            report_end = config.get('DATE', 'END')
        else:
            report_end = args.end
        report_end = datetime.datetime.strptime(report_end, '%Y-%m-%d')

        if args.breaks is None:
            report_breaks = int(config.get('DATE', 'BREAKS'))
        else:
            report_breaks = args.breaks
        report_breaks = report_breaks * 60 * 60

    if config.has_section('LOCATION'):

        if args.start is None:
            report_lla = json.loads(config.get('LOCATION', 'LLA'))
            report_lla = [float(report_lla[0]), float(report_lla[1])]
        else:
            report_lla = [args.latitude, args.longitude]

        if args.end is None:
            report_radius = float(config.get('LOCATION', 'RADIUS'))
        else:
            report_radius = float(args.radius)

    if config.has_section('SOURCE'):
        if args.filepath is None:
            filepath = config.get('SOURCE', 'FILEPATH')
        else:
            filepath = args.filepath

    geolocator = Nominatim()
    location = geolocator.reverse(report_lla)

    # prints information
    print('Google Maps Location History Parser')
    print('')
    print('author: PFigs')
    print('')
    print('reading from: {0}'.format(filepath))
    print('center set to: {0} ({1})'.format(
        location.address, report_lla))
    print('radius set to: {0}m'.format(report_radius))
    print('looking up during: {0} - {1}'.format(report_start, report_end))

    # Creates and initiates parser
    lochist = LocationHistory(filepath)

    lochist.inspect_date(report_start, report_end)
    lochist.inspect_distance(report_lla)
    lochist.filter_by_radius(report_radius)

    lochist.build_report(report_start, report_end, report_breaks)
    lochist.breakdown()

    lochist.write()

if __name__ == "__main__":

    main()