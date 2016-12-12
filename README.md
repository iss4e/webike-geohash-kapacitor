# WeBike GeoHash Processing using Kapacitor

This script provides a Kapacitor UDF node that accepts a stream of points containing GPS latitute and longitudes and 
adds the [geohash](https://pypi.python.org/pypi/python-geohash/0.8.5) of that coordinates to the points.

For more information on custom UDF nodes, see the 
[Kapacitor tutorial](https://docs.influxdata.com/kapacitor/v1.1/examples/anomaly_detection/).

The `kapacitor_udf` library can also be installed from the Kapacitor 
[source repo](https://github.com/influxdata/kapacitor/tree/master/udf/agent/py/), but requires slight modfications to run the the version of python installed on tornado (see the diff of the file agent.py).

## Installation

~~~
# Clone this script
git clone git@github.com:iss4e/webike-geohash-kapacitor.git
cd webike-geohash-kapacitor
# Create, enable and set-up a new virtual environment
pyvenv-3.5 venv
source venv/bin/activate
python setup.py develop

# Get path for installed geohash script
which geohash.py

# Make everything executable for the kapacitor user and leave venv
chown kapacitor . -Rv
chmod +r . -Rv
deactivate
~~~

Add this snippet to your Kapacitor configuration file (typically located at `/etc/kapacitor/kapacitor.conf`):
~~~
[udf]
[udf.functions]
    [udf.functions.geohash]
        # Run script (should be the output of $(which geohash.py) )
        prog = "/etc/kapacitor/scripts/venv/bin/geohash.py"
        # If the python process is unresponsive for 10s kill it
        timeout = "10s"
~~~

In the configuration we called the function geohash. That is also how we will reference it in the TICKscript.

Restart the Kapacitor process with `service kapacitor restart` and check that the geohash Agent shows up in the 
Kapacitor log in `/var/log/kapacitor/`.

Define the tick script using 
~~~
kapacitor define webike-geohash -type stream -dbrp webike.autogen -tick webike-geohash.tick
~~~
and then enable it using `kapacitor enable webike-geohash`.
