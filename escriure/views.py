import time
from collections import OrderedDict

from flask import abort, render_template, g, request, redirect, url_for, Response
from flask.ext.classy import FlaskView, route

from .models import *

class PostView(FlaskView):
    route_base = '/'
    
    @route('/<permaid>', endpoint='PostView:get_deprecated')
    @route('/post/<permaid>', endpoint='PostView:get')
    def get(self, permaid):
        post = PostModel.query.filter(PostModel.permaid == permaid, PostModel.status == 'published').first()
        
        if post == None:
            abort(404)
            
        if request.endpoint == 'PostView:get_deprecated':
            return redirect(g.config['url'] + url_for('PostView:get', permaid=permaid))
        
        g.session['canonical'] = post.custom['permalink']
        g.session['tags'] = post.tags
        g.session['title'] = post.title
        
        return render_template('postview.html', posts=[post])
        
class PageView(FlaskView):
    route_base = '/'
    
    @route('/', endpoint='PageView:front_page')
    @route('/page/<int:page>', endpoint='PageView:get')
    def get(self, page=1):
        query = PostModel.query.filter(PostModel.status == 'published').order_by('id desc')
        pagination = query.paginate(page, int(g.config['page_size']))
        posts = pagination.items
        
        if posts == None:
            abort(404)
            
        if page == 1:
            g.session['canonical'] = g.config['url'] + url_for('PageView:front_page')
        else:
            g.session['canonical'] = g.config['url'] + url_for('PageView:get', page=page)
            
        return render_template('postview.html', posts=posts, pagination=pagination)
        
class RSSView(FlaskView):
    route_base = '/'
    
    @route('/rss', endpoint='RSSView')
    @route('/rss/twitter', endpoint='RSSTwitterView')
    def get(self):
        if request.endpoint == 'RSSView':
            posts = PostModel.query.filter(PostModel.status == 'published').order_by('id desc').limit(int(g.config['page_size']) * 4)
        elif request.endpoint == 'RSSTwitterView':
            posts = PostModel.query.filter(PostModel.status == 'published', PostModel.twitter == 1).order_by('id desc').limit(int(g.config['page_size']) * 4)
        
        if posts == None:
            abort(404)
            
        return render_template('rss-postview.html', posts=posts)
        
class SitemapView(FlaskView):
    route_base = '/'
    
    @route('/sitemap.xml')
    def get(self):
        posts = PostModel.query.filter(PostModel.status == 'published').order_by('id desc')
        
        if posts == None:
            abort(404)
            
        return render_template('sitemap.xml', posts=posts)
        
class RestView(FlaskView):
    route_base = '/'
    
    @route('/robots.txt', endpoint='RobotsView')
    @route('/favicon.ico', endpoint='FaviconView')
    def get(self):
        if request.endpoint == 'RobotsView':
            robots = 'Sitemap: %s/sitemap.xml' % g.config['url']
            response = Response(response=robots, mimetype='text/plain')
            return response
        elif request.endpoint == 'FaviconView':
            return redirect(url_for('static', filename='favicon.png'))

class BlobView(FlaskView):
    route_base = '/'
    
    @route('/blob/<name>')
    def get(self, name):
        blob = BlobModel.query.filter(BlobModel.name == name).first()
        
        if blob == None:
            abort(404)
        
        response = Response(response=blob.content, mimetype=blob.mimetype)
        return response

class ArchiveView(FlaskView):
    route_base = '/'

    @route('/archive')
    def get(self):
        posts = PostModel.query.filter(PostModel.status == 'published').order_by('id desc')

        if posts == None:
            abort(404)

        archive = OrderedDict({})
        for post in posts:
            year = str(post.custom['datetime'].year)
            month = str(time.strftime('%B', post.custom['localtime']))
            if not year in archive:
                archive[year] = OrderedDict({})
            if not month in archive[year]:
                archive[year][month] = OrderedDict({})
                archive[year][month]['posts'] = []
            archive[year][month]['posts'].append(post)

        return render_template('archiveview.html', archive=archive)