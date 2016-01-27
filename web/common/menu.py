from flask import render_template, request
from htmlmin.main import minify

class MenuClass(object):
    def __init__(self, title = None, home = None):
        self.title = title if title else 'ACS Monitor'
        self.home = home if home else 'ACS Monitor'
        self.menu = dict()

    def add(self, name, url, group = None, description = None):
        item = { 'name' : name, 'url' : url, 'itemtype' : 'item', 'description' : description }
        if group:
            if group not in self.menu: self.menu[group] = dict( itemtype = 'group' )
            self.menu[group][url] = item
        else:
            self.menu[url] = item
        def decorator(method):
            return method
        return decorator

    def render(self, template, **kwargs):
        return minify(render_template(template, title = self.title, home = self.home, endpoint = request.endpoint, menu = self.menu, **kwargs))
