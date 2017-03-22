from novnc import proxy
from novnc.config import config

CONF = config.CONF


def main():
    CONF(default_config_files=['/etc/contrail/novnc.conf'])
    CONF.set_default('web', '/usr/share/novnc')

    proxy.proxy(
        host=CONF.host,
        port=CONF.port
    )