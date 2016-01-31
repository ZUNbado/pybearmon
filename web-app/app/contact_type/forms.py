import wtforms

class ContactForm(wtforms.Form):
    name = wtforms.TextField('Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])

class AttributeForm(wtforms.Form):
    name = wtforms.TextField('Name', [wtforms.validators.Required()])
    type = wtforms.TextField('Type', [wtforms.validators.Required()])
    required = wtforms.BooleanField('Required')
