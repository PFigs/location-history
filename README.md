# GMAPS Location History parser

Simple classes to deal with GMAPS location history files.

The goal is to understand how much time you spend in a given 
area based on a center point and a radius around it.

This script requires:

- GMAPS location history in JSON format (get it from takeout);


# Settings

You can customize the runtime parameters by:

- command line arguments;

- configuration file.

Command line definitions take precedence and overwrite what is 
defined in a configuration file.


# Configuration File
A configuration file can contain the following section and attributes
```
[SOURCE]
FILEPATH = ./location_history.json

[DATE]
# Break is set in hours
START = 2017-01-01
END = 2017-02-01
BREAKS = 1

[LOCATION]
# radius is set in meters
RADIUS = 50
LLA = [61, 23]
```


# Contributing
Feel free to send me pull requests
