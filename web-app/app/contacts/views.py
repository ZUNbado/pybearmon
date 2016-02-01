from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from app.common.forms import getFormForModelAttr
from .forms import ContactForm
from .controllers import Contacts
from app.contact_type.controllers import ContactType, ContactAttribute
from flask_menu import Menu, register_menu
from flask.ext.login import fresh_login_required
import urllib

from app.auth.utils import user_logged, user_admin
from app.contact_type.controllers import ContactType, ContactAttribute

app = Blueprint('contacts', __name__, url_prefix = '/contacts')
@app.route('/')
@register_menu(app, '.contacts.contacts_list', 'List', visible_when=user_logged)
@register_menu(app, '.contacts', 'Contacts', visible_when=user_logged)
@fresh_login_required
def contacts_list():
    contacts = Contacts().getAll()
    columns = [ 'name', 'contact_type' ]
    return render_template('list.html', items = contacts, columns = columns, endpoint = 'contacts' )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.contacts.contacts_edit', 'Add', visible_when=user_logged)
@fresh_login_required
def contacts_edit(id = None):
    form = getFormForModelAttr(ContactForm, Contacts, ContactAttribute, id, 'contacttype_id')
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
    return render_template('edit.html', form = form)


@app.route('/delete/<int:id>')
@fresh_login_required
def contacts_delete(id):
    Contacts().delete(id)
    return redirect(url_for('.contacts_list'))
