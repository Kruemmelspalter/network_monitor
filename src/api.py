import struct

from server import app
import network
import flask
import math


@app.route('/api')
def api():
    result = all([not host.fail for host in network.hosts])
    for i, host in enumerate(network.hosts):
        if not host.fail:
            result |= int(math.pow(2, i+1))
    return struct.pack(">I", result)
