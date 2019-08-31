"""
    Utils

    This module contains a general purpose classes to handle
    encoding, time, among other things.

"""

import argparse
import json
import datetime
import geopy
import yaml


def serialize(obj) -> str:
    """ Serializes an object into json """
    return json.dumps(obj, cls=DateTimeEncoder, sort_keys=True, indent=4)


class DateTimeEncoder(json.JSONEncoder):
    """ JSON encoder that handles datetime serialization """

    # pylint: disable=E0202
    # pylint: disable=W0221
    def default(self, obj):

        if isinstance(obj, (datetime.date, datetime.datetime)):
            obj = obj.isoformat()
            return obj

        if isinstance(obj, (geopy.Point)):
            return str([obj.latitude, obj.longitude, obj.altitude])

        if isinstance(obj, argparse.ArgumentParser):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

    # pylint: enable=E0202
    # pylint: enable=W0221


class Settings(object):
    """Simple class to handle library settings"""

    def __init__(self, settings: dict):
        super(Settings, self).__init__()
        for key, value in settings.items():
            self.__dict__[key] = value

    def items(self):
        """ Returns all the setting items """
        return self.__dict__.items()

    @classmethod
    def from_args(cls, args, skip_undefined=True):
        """ Returns a setting arguments based on the arguments input """
        settings = dict()

        try:
            if args.settings:
                with open(args.settings, "r") as settings_file:
                    settings = yaml.load(settings_file, Loader=yaml.FullLoader)
        except IOError:
            pass

        for key, value in args.__dict__.items():
            if value is not None or skip_undefined is False:
                if key in settings and settings[key] is None:
                    settings[key] = value
                if key not in settings:
                    settings[key] = value

        return cls(settings)

    def __str__(self):
        return str(self.__dict__)


class ParserHelper(object):
    """
    ParserHelper
    Handles the creation and decoding of arguments
    """

    def __init__(
        self,
        description="timemap arguments",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    ):
        super(ParserHelper, self).__init__()
        self._parser = argparse.ArgumentParser(
            description=description, formatter_class=formatter_class
        )
        self._groups = dict()
        self._arguments = None
        self._unknown_arguments = None

    @property
    def parser(self):
        """ Returns the parser object """
        return self._parser

    @property
    def arguments(self):
        """ Returns arguments that it can parse and throwing an error otherwise """
        self._arguments, self._unknown_arguments = self.parser.parse_known_args()
        return self._arguments

    @property
    def known_arguments(self):
        """ returns the unknown arguments it could not parse """
        return self._arguments

    @property
    def unkown_arguments(self):
        """ returns the unknown arguments it could not parse """
        return self._unknown_arguments

    def settings(self, settings_class=None, skip_undefined=True) -> "Settings":
        """ Parses arguments into a settings class """

        if settings_class is None:
            settings_class = Settings

        settings = settings_class.from_args(self.arguments, skip_undefined)

        return settings

    def __getattr__(self, name):
        if name not in self._groups:
            self._groups[name] = self._parser.add_argument_group(name)

        return self._groups[name]

    def add_file_settings(self):
        """ For file setting handling"""
        self.file_settings.add_argument(
            "--settings",
            type=str,
            required=False,
            default="defaults.yml",
            help="settings file.",
        )

    def dump(self, path):
        """ dumps the arguments into a file """
        with open(path, "w") as dump_file:
            dump_file.write(serialize(vars(self._arguments)))

    @classmethod
    def default_args(cls, text="Time map arguments") -> "ParserHelper":
        """ Provides default arguments """
        parse = cls(description=text)
        parse.add_file_settings()
        return parse

    def __str__(self):
        return serialize(self.__dict__)
