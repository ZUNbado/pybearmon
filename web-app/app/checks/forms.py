import wtforms
from app.common.forms import SubmitForm

class CheckForm(SubmitForm):
    name = wtforms.TextField('Check Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])
    type = wtforms.SelectField('Check Type', [wtforms.validators.Required()], coerce = int)
    max_confirmations = wtforms.IntegerField('Confirmations')
    public = wtforms.BooleanField('Is public?')
    contacts = wtforms.SelectMultipleField('Contacts', coerce = int, choices = list())
