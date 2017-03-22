from oslo_config import cfg

host_opt = cfg.StrOpt('host',
                      default="0.0.0.0",
                      help="The host vnc proxy will listen")

port_opt = cfg.IntOpt('port',
                      default='6080',
                      help='The port the vnc proxy will listen')

web_opt = cfg.StrOpt('web',
                     default="/usr/share/novnc",
                     help="The vnc web directory.")


CONF = cfg.CONF

CONF.register_opt(host_opt)
CONF.register_opt(port_opt)

CONF.register_opt(web_opt)




