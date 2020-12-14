import time
import json
import re
import dns.resolver
import pythonping
import socket
import requests

REGEX_IPV4 = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
REGEX_PORT = '^(?:[0-5]?[0-9]{1,4}|6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3})$'
REGEX_HTTP_METHOD = '(?i)^GET|HEAD|POST|PUT|DELETE|OPTIONS|PATCH$'
REGEX_PATH = '^\\/(?:[\\w\\?=]\\/?)*$'

hosts = []
CONF = {}

with open('conf/conf.json') as f:
    CONF = json.load(f)
    f.close()


class NotInConfigException(Exception):
    pass


class Host:
    def __init__(self, ip, hostname=None, checks=None):
        if checks is None:
            checks = {}
        self.ip = ip

        if re.match(REGEX_IPV4, ip) is None:
            raise ValueError(self.ip, " is not a valid ip address")

        if ip not in CONF['hosts'].keys():
            raise NotInConfigException(self.ip, " isn't registered as host")

        self.checks = {**checks, **{check: False for check in CONF['hosts'][ip]['checks']}}

        self.hostname = hostname or dns.resolver.resolve(dns.reversename.from_address(ip), 'PTR')[0].to_text()

        self.fail = True

    def check(self):
        for check_str in self.checks:
            check = check_str.split(':')
            if check[0] == 'ping':
                self.checks[check_str] = pythonping.ping(self.ip, count=1).success()

            elif check[0] == 'port':
                if re.match(REGEX_PORT, check[1]) is None:
                    raise ValueError(check[1], "is not a valid port (ip: '", self.ip + "', check: '", check_str, "'")

                self.checks[check_str] = check_port(self.ip, check[1])

            elif check[0] == 'http':
                if re.match(REGEX_PORT, check[1]) is None:
                    raise ValueError(check[1], "is not a valid port " +
                                     "(ip: '", self.ip + "', check: '", check_str, "'")
                if re.match(REGEX_HTTP_METHOD, check[2]) is None:
                    raise ValueError(check[2], "is not a valid HTTP method " +
                                     "(ip: '", self.ip + "', check: '", check_str, "'")
                if re.match(REGEX_PATH, check[3]) is None:
                    raise ValueError(check[3], "is not a valid path " +
                                     "(ip: '", self.ip + "', check: '", check_str, "'")
                if not check_port(self.ip, check[1]):
                    self.checks[check_str] = False
                    continue
                self.checks[check_str] = getattr(requests, check[2].lower())(
                    'http://' + self.ip + ':' + check[1] + check[3]).status_code == 200

            else:
                raise ValueError(check[0], "is not a valid check")
            self.fail = not all(self.checks.values())


def __str__(self):
    return "Host " + self.ip


def check_port(ip, port):
    if not isinstance(port, int):
        port = int(port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0


def init_hosts():
    global hosts
    for host_ip in CONF['hosts']:
        hosts.append(Host(host_ip))
    check_hosts()


def check_hosts():
    for host in hosts:
        host.check()


def reload_conf():
    global CONF
    with open('conf/conf.json') as f:
        CONF = json.load(f)
        f.close()
    hosts.clear()
    init_hosts()
    check_hosts()


def check_routine():
    print("routine")
    while True:
        print("check")
        check_hosts()
        time.sleep(CONF["sleep_delay"])


if __name__ == '__main__':
    init_hosts()
    print(hosts)
