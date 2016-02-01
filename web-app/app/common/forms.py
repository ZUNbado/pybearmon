import wtforms
from flask import request

def getFormForModel(Form, Model, id):
    form = Form(request.form)
    if id and request.method != 'POST':
        obj = Model().get(id)
        if obj:
            for key, value in obj.__dict__.items():
                field = getattr(form, key, None)
                if field:
                    field.data = value
                    setattr(form, key, field)
    return form
