import os
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme_file = "README.md"
license_file = "LICENSE"

with open(readme_file) as f:
    long_description = f.read()


def get_list_files(root, flist=None):
    if flist is None:
        flist = list()

    for path, subdirs, files in os.walk(root):
        for name in files:
            flist.append(os.path.join(path, name))
    return flist


def get_absolute_path(*args):
    """ Transform relative pathnames into absolute pathnames """
    return os.path.join(here, *args)


def get_requirements(*args):
    """ Get requirements requirements.txt """
    requirements = set()
    with open(get_absolute_path(*args)) as handle:
        for line in handle:
            # Strip comments.
            line = re.sub(r"^#.*|\s#.*", "", line)
            if "-" in line[0]:
                continue
            # Ignore empty lines
            if line and not line.isspace():
                requirements.add(re.sub(r"\s+", "", line))
    return sorted(requirements)


about = {}
with open(get_absolute_path("./timemap/__about__.py")) as f:
    exec(f.read(), about)

setup(
    name=about["__pkg_name__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    setup_requires=["setuptools_scm"],
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "version_scheme": "python-simplified-semver",
        "local_scheme": "no-local-version",
    },
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    classifiers=about["__classifiers__"],
    keywords=about["__keywords__"],
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=get_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["timemap-report=timemap.__main__:location_report"]
    },
)
