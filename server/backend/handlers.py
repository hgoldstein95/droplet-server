import logging
import SimpleHTTPServer

logger = logging.getLogger("ServerLogger")


class WebsiteHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        logger.info(format % args)
