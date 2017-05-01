#!/usr/bin/env python
# encoding: UTF-8

import os
from setuptools import setup, find_packages

from simple_screencast import VERSION


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()
elif os.path.isfile("README.md"):
    long_description = open("README.md", "r").read()


setup(
    name="simple_screencast",
    version=VERSION,
    description="Simple screen recording application for GNOME Shell",
    url="https://github.com/flozz/simple-screencast",
    license="GPLv3",

    long_description=long_description,

    author="Fabien LOISON",

    keywords="screencast screen recording video gnome",
    platforms=["Linux"],

    packages=find_packages(),
    include_package_data=True,

    entry_points={
        "console_scripts": [
            "simple-screencast = simple_screencast.__main__:main"
        ]
    }
)

