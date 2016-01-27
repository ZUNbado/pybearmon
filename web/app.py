from flask import Flask, render_template, request, redirect, url_for
from common.sql import getdb
from common.menu import MenuClass
from common.forms import CheckForm
from common.checks import Checks

app = Flask(__name__)
menu = MenuClass(title = 'ACS Status', home = 'ACS Status')

@menu.add('Add', '/checks/edit', 'Checks')
@app.route('/checks/edit', methods = [ 'POST', 'GET' ])
@app.route('/checks/edit/<int:id>', methods = [ 'POST', 'GET' ])
def checks_edit(id = None):
    form = CheckForm(request.form)
    if request.method == 'POST' and form.validate():
        check = Checks().save(id = id, name = form.name.data, type = form.type.data, data = form.data.data)
        if check:
            return redirect(url_for('checks_edit', id = check))
    else:
        if id:
            dbcheck = Checks().get(id)
            if dbcheck:
                form.name.data = dbcheck.name
                form.type.data = dbcheck.type
                form.data.data = dbcheck.data
    return menu.render('checks/edit.html', form = form)


@app.route('/')
def index():
    db = getdb()
    list_checks = db.getAll('checks')
    return menu.render('index.html', checks = list_checks if list_checks else [] )

if __name__ == '__main__':
    app.config.from_object('config.Development')
    app.run(debug=True)
