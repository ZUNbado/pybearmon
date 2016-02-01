from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from .forms import ContactForm, AttributeForm
from .controllers import ContactType, ContactAttribute
from flask_menu import Menu, register_menu
from flask.ext.login import fresh_login_required

from app.auth.utils import user_admin

app = Blueprint('contacts_type', __name__, url_prefix = '/contacts_type')
@app.route('/')
@register_menu(app, '.contactstype.contacttype_list', 'List', visible_when=user_admin)
@register_menu(app, '.contactstype.', 'Contact Types', visible_when=user_admin)
@fresh_login_required
def contacttype_list():
    contacts = ContactType().getAll()
    return render_template('list.html', items = contacts, columns = [ 'name' ], endpoint = 'contacttype' )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.contactstype.contacttype_edit', 'Add', visible_when=user_admin)
@fresh_login_required
def contacttype_edit(id = None):
    form = ContactForm(request.form)
    if form.validate_on_submit():
        contact = ContactType().save(id = id, name = form.name.data)
        if contact:
            return redirect(url_for('.contacttype_edit', id = contact))
    else:
        if id:
            dbcontact = ContactType().get(id)
            if dbcontact:
                form.name.data = dbcontact.name
    if id:
        attrs = ContactAttribute().getAll(contacttype_id = id)
    else:
        attrs = list()
    return render_template('contacttype/edit.html', form = form, attrs = attrs, id = id)

@app.route('/delete/<int:id>')
@fresh_login_required
def contacttype_delete(id):
    return redirect(url_for('.contacttype_list'))

@app.route('/delete/<int:contacttype_id>/attribute/<int:id>')
@fresh_login_required
def contactattribute_delete(contacttype_id, id):
    return redirect(url_for('.contacttype_edit', id = contacttype_id))

@app.route('/edit/<int:contacttype_id>/attribute', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:contacttype_id>/attribute/<int:id>', methods = [ 'POST', 'GET' ])
@fresh_login_required
def contactattribute_edit(contacttype_id, id = None):
    form = AttributeForm(request.form)
    if request.method == 'POST' and form.validate():
        attr = ContactAttribute().save(id = id, id_contact_type = contacttype_id, name = form.name.data, type = form.type.data, required = form.required.data)
        if attr:
            return redirect(url_for('.contacttype_edit', id = contacttype_id))
    else:
        if id:
            attr = ContactAttribute().get(id)
            if attr:
                for key, value in attr.__dict__.items():
                    if hasattr(form, key):
                        fd = getattr(form, key)
                        fd.data = value
                        setattr(form, key,  fd)
    return render_template('edit.html', form = form)
