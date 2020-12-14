import flask

import network

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html', title="Network Dashboard", hosts=network.hosts)


@app.route('/hosts')
def host_route():
    ip = flask.request.args.get('ip')
    return flask.render_template('host.html', host=[host for host in network.hosts if host.ip == ip][0])


@app.route('/reload')
def reload():
    network.reload_conf()
    return flask.redirect('/')


@app.route('/api/check')
def api_check():
    return "", 200 if all([not host.fail for host in network.hosts]) else 500


def run():
    app.run(port=80, host="172.19.0.2")
