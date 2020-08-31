# Timemap

A python package to deal with location history files, such
as GMAPS takeout json.

The main motivation behind this package is to allow simple analytics
based on where you have been, for example, how long did you spend
at the office over January?


Supported providers:
* Google - takeout's json


## Settings

You can customize the runtime parameters through a configuration file
or command line parameters (requires extension).


# Configuration File
The configuration consist of a yaml file. All the items in it, will be
exposed as settings to your script. 

Please see an example from [defaults.yaml][defaults.yaml].


## Getting a monthly report 

One use case for this package is to provide you an estimate of how may hours
you have spent around a given location, for example, how much time
you spent at the office.

To obtain a report you need to:

1. Download your location history from [Google's takeout service][takeout];
1. Unzip it and copy the location history file into ./input folder (git ignored);
1. Copy [defaults.yaml][defaults.yaml] and update the path and coordinates accordingly (note that input is mounted as /data/ inside the container);
1. Start the entrypoint using docker-compose run timemap or locally with timemap-report


# Contributing
Feel free to send me your pull requests and create issues for your ideas.

[defaults.yaml]: https://github.com/PFigs/location-history/blob/master/tests/defaults.yml
[takeout]: https://takeout.google.com