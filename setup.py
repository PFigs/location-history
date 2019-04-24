import codecs
import os
import re
import glob

from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

with open("LICENSE") as f:
    license = f.read()


def filter(flist, rules=["private", ".out"]):
    for f in flist:
        for rule in rules:
            if rule in f:
                flist.pop(flist.index(f))
    return flist


def get_list_files(root, flist=None):
    if flist is None:
        flist = list()

    for path, subdirs, files in os.walk(root):
        for name in files:
            flist.append(os.path.join(path, name))
    return flist


def get_absolute_path(*args):
    """ Transform relative pathnames into absolute pathnames """
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, *args)


def get_requirements(*args):
    """ Get requirements requirements.txt """
    requirements = set()
    with open(get_absolute_path(*args)) as handle:
        for line in handle:
            # Strip comments.
            line = re.sub(r"^#.*|\s#.*", "", line)
            # Ignore empty lines
            if line and not line.isspace():
                requirements.add(re.sub(r"\s+", "", line))
    return sorted(requirements)


setup(
    name="timemap",
    version="0.0.1",
    description="Location history parser and analyzer",
    long_description=long_description,
    author="PFigs",
    author_email="noreply@pfigs.com",
    url="https://github.com/pfigs/timemap",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
    ],
    keywords="maps location time tracking",
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=get_requirements("requirements.txt"),
)
