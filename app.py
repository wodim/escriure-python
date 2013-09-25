from flask import Flask, render_template, request, g, flash, session
from flask_gzip import Gzip

from escriure.config import _cfg, _cfgc
from escriure.database import db

from escriure.models import PostModel
from escriure.views import PostView, PageView, RSSView, SitemapView, RestView

import time

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = _cfg('database')
db.app = app
db.init_app(app)
Gzip(app)

PostView.register(app)
PageView.register(app)
RSSView.register(app)
SitemapView.register(app)
RestView.register(app)

@app.before_request
def before_request():
    g.start = time.time()
    g.config = _cfgc
    g.session = {}
    
@app.after_request
def after_request(response):
    # required by autogzip
    response.direct_passthrough = False
    # calculate request time. hackkkk
    diff = time.time() - g.start
    if (response.response and response.content_type.startswith('text/html') and response.status_code==200):
        response.response[0] = response.response[0].replace('__TIME__', str(diff))
        response.headers["content-length"] = len(response.response[0])
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)