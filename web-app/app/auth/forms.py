from flask.ext.wtf import Form
import wtforms

class LoginForm(Form):
    email = wtforms.TextField('Email', [wtforms.validators.Required()])
    password = wtforms.PasswordField('Password', [wtforms.validators.Required()])

class RegisterForm(Form):
    name = wtforms.StringField('User name', [wtforms.validators.Required()])
    email = wtforms.StringField('Email', [wtforms.validators.Email(), wtforms.validators.Required()])
    password = wtforms.PasswordField('Password', [wtforms.validators.Required(), wtforms.validators.EqualTo('password_confirm')])
    password_confirm = wtforms.PasswordField('Confirm Password')
