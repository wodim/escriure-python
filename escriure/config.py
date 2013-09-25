from ConfigParser import ConfigParser

config = ConfigParser()
config.readfp(open('config.ini'))

# i dont really need this
_cfg = lambda k: config.get('escriure', k)
_cfgi = lambda k: int(_cfg(k))
_cfgc = dict(config.items('escriure'))