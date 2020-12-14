import threading

import network
import server

if __name__ == '__main__':
    network.init_hosts()
    threads = [threading.Thread(target=network.check_routine), threading.Thread(target=server.run)]
    for thread in threads:
        thread.start()
