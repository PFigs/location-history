# -*- coding: utf-8 -*-
"""
Writing gmaps data into influxdb

"""
import json
import ijson
import argparse
import datetime

from influxdb import InfluxDBClient


class LoctionDatabaseHandler(object):
    """docstring for LoctionImporter"""
    def __init__(self, filepath, kwargs):
        super(LoctionDatabaseHandler, self).__init__()
        
        self.filepath = filepath
        self._fd = open(self.filepath, 'r')
        self._parser = ijson.parse(self._fd)

        self.client = None

        self.establish_connection(kwargs)


    def _default_body(self):
        return  { 'measurement': None,
                   'tags': None,
                   'time': None,
                   'fields': None
                }
        
    def writetodb(self, start=None, end=None):
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

        
        
        # streams in json file and build point based on timestamp,
        # latitude and longitude.
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
            
            elif prefix.endswith('.accuracy'):
                accuracy = value

            elif prefix.endswith('.altitude'):
                altitude = value
            
            elif prefix.endswith('.verticalAccuracy'):
                accuracy_vertical = value
                complete = True

            else:
                continue

            if complete is True:
                complete = False
                payload = self._default_body()
                payload['measurement'] = 'locations'
                payload['time'] = '{0}Z'.format(time.isoformat())
                payload['tags'] = {'latitude': latitude, 
                                   'longitude': longitude, 
                                   'altitude': altitude}
                payload['fields'] = {'accuracy': accuracy, 'accuracy_vertical': accuracy_vertical}
                self.write([payload])
    

    def establish_connection(self, dboptions):    
        self.connection = InfluxDBClient(dboptions.host, 
                                             dboptions.port, 
                                             dboptions.dbuser, 
                                             dboptions.dbuser_password, 
                                             dboptions.dbname)




    def write(self, payload):
        """ writes the provided data"""
        self.connection.write_points(payload)

    def query(self, what, from_where):
        """ Provides a simple SELECT query from influx """
        return client.query('select {0} from {1}'.format(what, from_where))

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', 
                        type=str, 
                        required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API.')

    parser.add_argument('--port', 
                        type=int, 
                        required=False, 
                        default=8086,
                        help='port of InfluxDB http API.')

    parser.add_argument('--dbname', 
                        type=str, 
                        required=False, 
                        default="gmaps",
                        help='database name.')

    parser.add_argument('--dbuser', 
                        type=str, 
                        required=False, 
                        default="gmapsuser",
                        help='username to use in the database connection.')

    parser.add_argument('--dbuser_password', 
                        type=str, 
                        required=False, 
                        default="gmapspassword",
                        help='user''s password to use in the database connection.')

    parser.add_argument("--filepath", 
                        type=str,
                        required=True, 
                        help="Location history filepath.")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    locdb = LoctionDatabaseHandler(args.filepath, args)
    locdb.writetodb()
    #main(host=args.host, port=args.port)