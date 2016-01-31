import wtforms

class UserForm(wtforms.Form):
    name = wtforms.TextField('User Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])
    email = wtforms.TextField('Email', [wtforms.validators.Required(), wtforms.validators.length(min=4)])
    password = wtforms.PasswordField('Password', [wtforms.validators.Required()])