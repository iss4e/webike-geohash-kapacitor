# WeBike GeoHash Processing using Kapacitor

This script provides a Kapacitor UDF node that accepts a stream of points that contain GPS latitute and longitudes and 
adds the [geohash](https://pypi.python.org/pypi/python-geohash/0.8.5) of that coordinates to the points.

For more information on custom UDF nodes, see the 
[Kapacitor tutorial](https://docs.influxdata.com/kapacitor/v1.1/examples/anomaly_detection/).

The `kapacitor_udf` library can be installed from the Kapacitor 
[source repo](https://github.com/influxdata/kapacitor/tree/master/udf/agent/py/).

## Installation

Clone this script and run `python3 setup.py develop --user`

Add this snippet to your Kapacitor configuration file (typically located at `/etc/kapacitor/kapacitor.conf`):
~~~
[udf]
[udf.functions]
    [udf.functions.geohash]
        # Run python
        prog = "/usr/bin/python3"
        # Pass args to python
        # -u for unbuffered STDIN and STDOUT
        # and the path to the script
        args = ["-u", "/home/user/webike-geohash-kapacitor/iss4e/webike/geohash.py.py"]
        # If the python process is unresponsive for 10s kill it
        timeout = "10s"
        # Define env vars for the process, in this case the PYTHONPATH
        [udf.functions.tTest.env]
            PYTHONPATH = "/home/user/kapacitor_udf/kapacitor/udf/agent/py"
~~~

In the configuration we called the function geohash. That is also how we will reference it in the TICKscript.
Notice that our Python script imported the Agent object, and we set the PYTHONPATH in the configuration.
Clone the Kapacitor source into the tmp dir so we can point the PYTHONPATH at the necessary python code.
This is typically overkill since it’s just two Python files, but it makes it easy to follow:
~~~
git clone https://github.com/influxdata/kapacitor.git /tmp/kapacitor_udf/kapacitor
~~~

Restart the Kapacitor process with `# service kapacitor restart` and check that the geohash Agent show up in the 
Kapacitor log in `/var/log/kapacitor/`.

Call the UDF node like this:
~~~
var data = stream
    |from()
        .measurement('sensor_values')
    @geohash()
        .field_lat('latgps')
        .field_long('longgps')
    |influxDBOut()
        .database('webike')
        .measurement('geohashes')
~~~
