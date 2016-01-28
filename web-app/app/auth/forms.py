import wtforms

class LoginForm(wtforms.Form):
    email = wtforms.TextField('Email', [wtforms.validators.Required()])
    password = wtforms.PasswordField('Password', [wtforms.validators.Required()])
