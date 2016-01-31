from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from .forms import ContactForm
from .controllers import Contacts
from app.contact_type.controllers import ContactType, ContactAttribute
from flask_menu import Menu, register_menu
from flask.ext.login import current_user
import wtforms
import urllib
import urlparse

from app.auth.utils import user_logged, user_admin
from app.contact_type.controllers import ContactType, ContactAttribute

app = Blueprint('contacts', __name__, url_prefix = '/contacts')
@app.route('/')
@register_menu(app, '.contacts.contacts_list', 'List', visible_when=user_logged)
@register_menu(app, '.contacts', 'Contacts', visible_when=user_logged)
def contacts_list():
    contacts = Contacts().getAll()
    return render_template('contacts/list.html', items = contacts )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.contacts.contacts_edit', 'Add', visible_when=user_logged)
def contacts_edit(id = None):
    class ContactA(ContactForm):
        pass
    if id:
        contact = Contacts().get(id)
        data = urlparse.parse_qs(contact.data)
        attrs = ContactAttribute().getAll(contacttype_id = contact.type)
        for attr in attrs:
            value = data[attr.name][0] if attr.name in data else ''
            field = wtforms.TextField(attr.name, default = value)
            setattr(ContactA, 'attr_%s' % attr.name, field)


    form = ContactA(request.form)
    form.type.choices = ContactType().formList()
    if request.method == 'POST' and form.validate_on_submit():
        data = dict()
        for field in form:
            if field.id[:5] == 'attr_':
                data[field.id[5:]] = field.data
        data = urllib.urlencode(data)
        contact = Contacts().save(id = id, name = form.name.data, type = form.type.data, data = data)
        if contact:
            return redirect(url_for('.contacts_edit', id = contact))
    else:
        if id:
            dbcontact = Contacts().get(id)
            if dbcontact:
                form.type.default = dbcontact.type
                form.process()
                form.name.data = dbcontact.name
    return render_template('contacts/edit.html', form = form)


@app.route('/delete/<int:id>')
def contacts_delete(id):
    Contacts().delete(id)
    return redirect(url_for('.contacts_list'))
