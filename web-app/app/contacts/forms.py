from flask.ext.wtf import Form
import wtforms

class ContactForm(Form):
    name = wtforms.TextField('Contact Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])
    type = wtforms.SelectField('Contact Type', [wtforms.validators.Required()], coerce = int)
