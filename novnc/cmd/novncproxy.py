from novnc import proxy
from novnc.config import config
from oslo_log import log as logging

CONF = config.CONF


def main():
    CONF(default_config_files=['/etc/contrail/novnc.conf'])
    CONF.set_default('web', '/usr/share/novnc')

    logging.setup(CONF, "novnc-proxy")

    proxy.proxy(
        host=CONF.host,
        port=CONF.port
    )
