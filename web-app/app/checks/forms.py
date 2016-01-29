from flask.ext.wtf import Form
import wtforms

class CheckForm(Form):
    name = wtforms.TextField('Check Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])
    type = wtforms.SelectField('Check Type', [wtforms.validators.Required()], coerce = int)
