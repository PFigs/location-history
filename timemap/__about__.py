"""
    About Timemap

    This file contains the metadata that is appended to the
    python wheel file, upon the setup.py call.
"""

from pkg_resources import get_distribution, DistributionNotFound

__author__ = "Pedro Silva"
__author_email__ = "noreply@pfgis.com"
__classifiers__ = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 3",
]
__copyright__ = "2019 PFigs (Pedro Figueiredo e Silva)"
__description__ = "Location history parser and analyzer."
__license__ = "MIT"
__pkg_name__ = "timemap"
__title__ = "Time map"
__url__ = "https://github.com/pfigs/location-history"

__keywords__ = ("maps location time tracking",)


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
