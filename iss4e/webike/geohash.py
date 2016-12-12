import sys

import geohash

from iss4e.webike import udf_pb2
from iss4e.webike.agent import Agent, Handler


class GeohashHandler(Handler):
    def __init__(self, agent):
        self._agent = agent

        self._field_lat = self._field_long = None
        self._field_geohash = "geohash"
        self._keep_fields = self._keep_coords = False

    def info(self):
        """
        Respond with which type of edges we want/provide and any options we have.
        """
        response = udf_pb2.Response()
        # We will consume batch edges aka windows of data.
        response.info.wants = udf_pb2.STREAM
        # We will produce single points of data aka stream.
        response.info.provides = udf_pb2.STREAM

        # Here we can define options for the UDF.
        # Define which fields we should process
        response.info.options['field_lat'].valueTypes.append(udf_pb2.STRING)
        response.info.options['field_long'].valueTypes.append(udf_pb2.STRING)
        response.info.options['keep_fields'].valueTypes.append(udf_pb2.BOOL)
        response.info.options['keep_coords'].valueTypes.append(udf_pb2.BOOL)

        return response

    def init(self, init_req):
        """
        Given a list of options initialize this instance of the handler
        """
        success = True
        msg = ''
        for opt in init_req.options:
            if opt.name == 'field_lat':
                self._field_lat = opt.values[0].stringValue
            elif opt.name == 'field_long':
                self._field_long = opt.values[0].stringValue
            elif opt.name == 'field_geohash':
                self._field_geohash = opt.values[0].stringValue
            elif opt.name == 'keep_fields':
                self._field_geohash = opt.values[0].boolValue
            elif opt.name == 'keep_coords':
                self._field_geohash = opt.values[0].boolValue

        if not self._field_lat or not self._field_long:
            success = False
            msg += ' must supply a field_lat and field_long name'

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]

        return response

    def point(self, point):
        if not self._keep_fields:
            point.fieldsDouble = {k: v for k, v in point.fieldsDouble
                                  if k in [self._field_lat, self._field_long] and self._keep_coords}
            point.fieldsInt = {}
            point.fieldsString = {}

        point.fieldsString[self._field_geohash] = geohash.encode(
            point.fieldsDouble[self._field_lat],
            point.fieldsDouble[self._field_long]
        )

        # Send geohash point back to Kapacitor
        response = udf_pb2.Response()
        response.point = point
        self._agent.write_response(response)


if __name__ == '__main__':
    # Create an agent
    agent = Agent(
        _in=sys.stdin.buffer,
        out=sys.stdout.buffer,
    )

    # Create a handler and pass it an agent so it can write points
    h = GeohashHandler(agent)

    # Set the handler on the agent
    agent.handler = h

    # Anything printed to STDERR from a UDF process gets captured into the Kapacitor logs.
    print("Starting agent for WeBike Geohashes", file=sys.stderr)
    agent.start()
    agent.wait()
    print("Agent finished", file=sys.stderr)
