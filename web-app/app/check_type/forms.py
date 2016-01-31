import wtforms

class CheckForm(wtforms.Form):
    name = wtforms.TextField('Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])


choices = [
        ('TextField', 'Text'),
        ('BooleanField', 'Boolean'),
        ('IntegerField', 'Integer'),
        ('PasswordField', 'Password'),
        ]

class AttributeForm(wtforms.Form):
    name = wtforms.TextField('Name', [wtforms.validators.Required()])
    type = wtforms.SelectField('Type', choices = choices)
    required = wtforms.BooleanField('Required')
