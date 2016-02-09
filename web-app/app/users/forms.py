import wtforms
from app.common.forms import SubmitForm

class UserForm(SubmitForm):
    name = wtforms.TextField('User Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])
    email = wtforms.TextField('Email', [wtforms.validators.Required(), wtforms.validators.length(min=4)])
    password = wtforms.PasswordField('Password')
    is_active = wtforms.BooleanField('Active')
    is_admin = wtforms.BooleanField('Admin')
