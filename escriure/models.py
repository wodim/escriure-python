from database import db
from flask import g, url_for

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

    @property
    def custom(self):
        custom = {}
        custom['permalink'] = g.config['url'] + url_for('PostView:get', permaid=self.permaid)
        custom['date'] = time.strftime('%e %b %Y', time.localtime(self.timestamp))
        custom['date_full'] = time.strftime('%c', time.localtime(self.timestamp))
        custom['date_rss'] = time.strftime('%a, %d %b %Y %H:%M:%S %z', time.localtime(self.timestamp))
        
        return custom

    def __repr__(self):
        return '<Post %r, permaid %r>' % (self.id, self.permaid)

def markdown_convert(target, context):
    if target.text_type == 'markdown':
        # convertir
        # target.text_type = 'html'
        pass
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