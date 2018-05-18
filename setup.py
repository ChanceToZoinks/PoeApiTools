import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "PoEApiTools",
    version = "0.2.0",
    author = "Gabriel Akers",
    author_email = "gabe.akers17@gmail.com",
    description = "Various tools to interface with and do basic calculations on PoE related APIs ",
    license = "MIT",
    keywords = "POE path exile",
    url = "http://packages.python.org/PoEApiTools",
    packages = ['PoEApiTools'],
    long_description = read('README'),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6"
    ],
    install_requires = ['requests']
)
