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
START = 2017-01-01 # YYYY-MM-DD
END = 2017-02-01 # YYYY-MM-DD
BREAKS = 1 # dont count events spaced more than N hours apart

[LOCATION]
RADIUS = 50 # in meters
LLA = [61, 23]
```

# Running within Docker
This repository is kept in sync with Docker Hub with each master commit.

To obatin a hour report, replace the following command with the correct
path to your Location history data and your own settings ini file:

```
docker run --rm \
            -v $(pwd)/your_location_history.json:/app/location_history.json \
            -v $(pwd)/your_settings.ini:/app/defaults.ini \
            pfigs/location-history
	    
``

Alternatively you can pass in the desired time range using the command
line arguments.


# Contributing
Feel free to send me your pull requests
