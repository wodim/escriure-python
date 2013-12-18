import time

from flask import Flask, render_template, request, g, flash, session

from escriure.config import _cfg, _cfgc
from escriure.database import db
from escriure.views import *

app = Flask(__name__)
app.debug = True

# jinja2
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = _cfg('database')
db.app = app
db.init_app(app)

# register views
PostView.register(app)
PageView.register(app)
RSSView.register(app)
SitemapView.register(app)
RestView.register(app)
BlobView.register(app)
ArchiveView.register(app)

@app.before_request
def before_request():
    g.start = time.time()
    g.config = _cfgc
    if 'server_name' in g.config:
        g.config['url'] = 'http://%s' % (g.config['server_name'],)
    else:
        g.config['url'] = 'http://%s' % (app.config['SERVER_NAME'],)
    g.session = {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)