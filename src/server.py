import flask

import network
import threading

app = flask.Flask(__name__)

import api


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


@app.before_first_request
def activate_job():
    network.init_hosts()
    thread = threading.Thread(target=network.check_routine)
    thread.start()


def run():
    app.run(port=80)
