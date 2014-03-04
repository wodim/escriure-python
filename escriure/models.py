from database import db
from flask import g, url_for
from markdown import markdown
from datetime import datetime

import time

# -- POST MODEL --

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    permaid = db.Column(db.String(64), unique=True)
    nick = db.Column(db.String(16))
    timestamp = db.Column(db.Integer)
    title = db.Column(db.String(128))
    text_html = db.Column(db.Text)
    text_markdown = db.Column(db.Text)
    text_type = db.Column(db.Enum(['html', 'markdown']))
    tags = db.Column(db.String(128))
    status = db.Column(db.Enum(['draft', 'published']))
    comment_count = db.Column(db.Integer)
    comment_status = db.Column(db.Text)
    twitter = db.Column(db.Integer)

    @property
    def custom(self):
        custom = {}
        custom['permalink'] = url_for('PostView:get', permaid=self.permaid, _external=True)
        custom['datetime'] = datetime.fromtimestamp(self.timestamp) # used for archive generation
        custom['localtime'] = time.localtime(self.timestamp) # used for archive generation
        custom['date_archive'] = time.strftime('%e %B', custom['localtime']) # used for archive
        custom['date'] = time.strftime('%e %b %Y', custom['localtime']) # shown as timestamps
        custom['date_full'] = time.strftime('%c', custom['localtime']) # shown as tooltips in timestamps
        custom['date_rss'] = time.strftime('%a, %d %b %Y %H:%M:%S %z', custom['localtime']) # shown in rss feed
        return custom

    def __repr__(self):
        return '<Post %r, permaid %r>' % (self.id, self.permaid)

def markdown_convert(target, context):
    if target.text_type == 'markdown':
        target.text_html = markdown(target.text_markdown)
        target.text_type = 'html'
        db.session.commit()

db.event.listen(PostModel, 'load', markdown_convert)

# -- BLOB MODEL --

class BlobModel(db.Model):
    __tablename__ = 'blobs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    mimetype = db.Column(db.String(32))
    timestamp = db.Column(db.Integer)
    size = db.Column(db.Integer)
    content = db.Column(db.BLOB)

    def __repr__(self):
        return '<Blob %r, name %r, size %r, mimetype %s>' % (self.id, self.name, self.size, self.mimetype)

# -- CONFIGURATION MODEL --

class ConfigModel(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32))
    value = db.Column(db.String(32))

    def __repr__(self):
        return '<Config %r, key %r, value %r>' % (self.id, self.key, self.value)