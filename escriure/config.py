from ConfigParser import ConfigParser

from models import ConfigModel

config = ConfigParser()
config.readfp(open('config.ini'))

_cfg = lambda k: config.get('escriure', k)
_cfgi = lambda k: int(_cfg(k))
_cfgc = dict(config.items('escriure'))

_cfg_db = lambda k: ConfigModel.query.filter(ConfigModel.key == k).order_by('id desc').first()
_cfgi_db = lambda k: int(_cfg_db(k))
_cfgc_db = ConfigModel.query.all()