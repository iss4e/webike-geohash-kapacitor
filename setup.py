from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='webike-geohash-kapacitor',
    version='0.1.0',
    description='WeBike GeoHash Processing using Kapacitor',
    long_description=long_description,
    url='https://github.com/iss4e/webike-geohash-kapacitor',
    author='Simon Dominik `Niko` Fink',
    author_email='sfink@uwaterloo.ca',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(),
    install_requires=[
        'python-geohash>=0.8.5',
        'kapacitor_udf'  # install from https://github.com/influxdata/kapacitor/tree/master/udf/agent/py/
    ]
)
