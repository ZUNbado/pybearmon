import wtforms
from flask import request
import urlparse
from flask.ext.wtf import Form as FForm

class SubmitForm(FForm):
    submit = wtforms.SubmitField('Save')
    submit_return = wtforms.SubmitField('Save and return')

def getFormForModel(Form, Model, id):
    form = Form(request.form)
    if id and request.method != 'POST':
        obj = Model().get(id)
        if obj:
            for key, value in obj.__dict__.items():
                field = getattr(form, key, None)
                if field and type(field) != dict:
                    field.data = value
                    setattr(form, key, field)
    return form

def getFormForModelAttr(Form, Model, ModelAttr, id, search):
    class ModelAttrForm(Form):
        pass
    if id:
        obj = Model().get(id)
        data = urlparse.parse_qs(obj.data)
        attrs = ModelAttr().getAll(**{ search : obj.type })
        for attr in attrs:
            value = data[attr.name][0] if attr.name in data else ''
            validators = []
            if attr.required: validators.append(wtforms.validators.Required())
            field = getattr(wtforms, attr.type)(attr.name, default = value, validators = validators)
            setattr(ModelAttrForm, 'attr_%s' % attr.name, field)

    return getFormForModel(ModelAttrForm, Model, id)
