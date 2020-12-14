from server import app
import network


@app.route('/api')
def api():
    result = [all([not host.fail for host in network.hosts])] + [not host.fail for host in network.hosts]
    return b"".join([b"t" if b else b"f" for b in result])
