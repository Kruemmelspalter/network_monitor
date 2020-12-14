import threading

import network
from server import app as application

if __name__ == '__main__':
    network.init_hosts()
    threads = [threading.Thread(target=network.check_routine), threading.Thread(target=application.run)]
    for thread in threads:
        thread.start()
