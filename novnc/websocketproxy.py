# Copyright (c) 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

'''
Websocket proxy that is compatible with OpenStack Nova.
Leverages websockify.py by Joel Martin
'''

import socket
import sys

from oslo_log import log as logging
from six.moves import http_cookies as Cookie
import six.moves.urllib.parse as urlparse
import websockify
import exceptions
from base64 import decodestring
from json import loads


LOG = logging.getLogger(__name__)


class ProxyRequestHandlerBase(object):
    def new_websocket_client(self):
        """Called after a new WebSocket connection has been established."""
        # Reopen the eventlet hub to make sure we don't share an epoll
        # fd with parent and/or siblings, which would be bad

        from eventlet import hubs
        hubs.use_hub()

        # The nova expected behavior is to have token
        # passed to the method GET of the request
        parse = urlparse.urlparse(self.path)
        if parse.scheme not in ('http', 'https'):
            # From a bug in urlparse in Python < 2.7.4 we cannot support
            # special schemes (cf: http://bugs.python.org/issue9374)
            if sys.version_info < (2, 7, 4):
                raise exceptions(
                    ("We do not support scheme '%s' under Python < 2.7.4, "
                      "please use http or https") % parse.scheme)

        query = parse.query
        token = urlparse.parse_qs(query).get("token", [""]).pop()
        if not token:
            # NoVNC uses it's own convention that forward token
            # from the request to a cookie header, we should check
            # also for this behavior
            hcookie = self.headers.getheader('cookie')
            if hcookie:
                cookie = Cookie.SimpleCookie()
                cookie.load(hcookie)
                if 'token' in cookie:
                    token = cookie['token'].value


        # Verify Origin
        expected_origin_hostname = self.headers.getheader('Host')
        if ':' in expected_origin_hostname:
            e = expected_origin_hostname
            if '[' in e and ']' in e:
                expected_origin_hostname = e.split(']')[0][1:]
            else:
                expected_origin_hostname = e.split(':')[0]
        # expected_origin_hostnames = CONF.console_allowed_origins
        # expected_origin_hostnames.append(expected_origin_hostname)
        origin_url = self.headers.getheader('Origin')
        # missing origin header indicates non-browser client which is OK
        if origin_url is not None:
            origin = urlparse.urlparse(origin_url)
            origin_hostname = origin.hostname
            origin_scheme = origin.scheme
            if origin_hostname == '' or origin_scheme == '':
                detail = _("Origin header not valid.")
                raise exceptions(detail=detail)

        param_dict = loads(decodestring(token))

        host = param_dict["host"]
        port = int(param_dict["port"])
        tsock = self.socket(host, port, connect=True)

        try:
            self.do_proxy(tsock)
        except Exception:
            if tsock:
                tsock.shutdown(socket.SHUT_RDWR)
                tsock.close()
                self.vmsg(_("%(host)s:%(port)s: Target closed") %
                          {'host': host, 'port': port})
            raise


class ProxyRequestHandler(ProxyRequestHandlerBase,
                              websockify.ProxyRequestHandler):
    def __init__(self, *args, **kwargs):
        websockify.ProxyRequestHandler.__init__(self, *args, **kwargs)

    def socket(self, *args, **kwargs):
        return websockify.WebSocketServer.socket(*args, **kwargs)


class WebSocketProxy(websockify.WebSocketProxy):
    @staticmethod
    def get_logger():
        return LOG
