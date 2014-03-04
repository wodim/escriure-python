from flask import Flask, g

from escriure.views import *
from escriure.config import _cfgc, _cfgc_db

app = Flask(__name__)

# jinja2
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = _cfg('database')
app.config['SQLALCHEMY_ECHO'] = True
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
    g.config = _cfgc
    g.config_db = _cfgc_db
    g.session = {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
