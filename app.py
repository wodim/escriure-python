from flask import Flask, render_template, request, g, flash, session

from escriure.config import _cfg, _cfgc
from escriure.database import db

from escriure.views import *

import time

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = _cfg('database')
db.app = app
db.init_app(app)

PostView.register(app)
PageView.register(app)
RSSView.register(app)
SitemapView.register(app)
RestView.register(app)
BlobView.register(app)

@app.before_request
def before_request():
    g.start = time.time()
    g.config = _cfgc
    g.session = {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)