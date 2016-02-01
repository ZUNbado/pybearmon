from flask.ext.wtf import Form
import wtforms

class CheckForm(Form):
    name = wtforms.TextField('Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])


choices = [
        ('TextField', 'Text'),
        ('BooleanField', 'Boolean'),
        ('IntegerField', 'Integer'),
        ('PasswordField', 'Password'),
        ]

class AttributeForm(Form):
    name = wtforms.TextField('Name', [wtforms.validators.Required()])
    type = wtforms.SelectField('Type', choices = choices)
    required = wtforms.BooleanField('Required')
