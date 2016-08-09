#!/usr/bin/python

import sys
import SocketServer
import logging
import logging.handlers
import threading
import time
from backend.handlers import WebsiteHandler

logger = logging.getLogger("ServerLogger")


def init_logging():
    logger.setLevel(logging.INFO)

    fh = logging.handlers.TimedRotatingFileHandler(
        'logs/server.log',
        when='w6',
        interval=1,
        backupCount=5)
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        '%I:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)


class ServerThread(threading.Thread):

    def __init__(self, port, handler):
        threading.Thread.__init__(self)
        self.port = port
        self.handler = handler
        self.daemon = True

    def run(self):
        httpd = SocketServer.TCPServer(("", self.port), self.handler)
        httpd.serve_forever()

if __name__ == "__main__":
    init_logging()

    handlers = [(80, WebsiteHandler)]

    servers = []
    for (port, handler) in handlers:
        server = ServerThread(port, handler)
        servers.append(server)
        logger.info('Starting %s on port %i', handler.__name__, port)
        server.start()

    try:
        while len(servers) > 0:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.warning('Keyboard Interrupt. Shutting down')
        sys.exit()
