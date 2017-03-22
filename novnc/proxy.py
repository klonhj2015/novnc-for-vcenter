import sys

import websocketproxy
from novnc.config import config

CONF = config.CONF


def exit_with_error(msg, errno=-1):
    sys.stderr.write(msg + '\n')
    sys.exit(errno)


def proxy(host, port):

    websocketproxy.WebSocketProxy(
        listen_port=port,
        listen_host=host,
        source_is_ipv6=False,
        verbose=True,
        cert="self.pem",
        key=None,
        ssl_only=False,
        daemon=False,
        record=None,
        traffic=True,
        web=CONF.web,
        file_only=True,
        RequestHandlerClass=websocketproxy.ProxyRequestHandler
    ).start_server()
