import wtforms
from app.common.forms import SubmitForm

class ContactForm(SubmitForm):
    name = wtforms.TextField('Contact Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])
    type = wtforms.SelectField('Contact Type', [wtforms.validators.Required()], coerce = int)
