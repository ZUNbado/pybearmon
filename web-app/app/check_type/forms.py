from app.common.forms import SubmitForm
import wtforms

class CheckForm(SubmitForm):
    name = wtforms.TextField('Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])


choices = [
        ('TextField', 'Text'),
        ('BooleanField', 'Boolean'),
        ('IntegerField', 'Integer'),
        ('PasswordField', 'Password'),
        ]

class AttributeForm(SubmitForm):
    name = wtforms.TextField('Name', [wtforms.validators.Required()])
    type = wtforms.SelectField('Type', choices = choices)
    required = wtforms.BooleanField('Required')
