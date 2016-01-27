import wtforms

class CheckForm(wtforms.Form):
    name = wtforms.TextField('Check Name', [wtforms.validators.Required(), wtforms.validators.length(min=4)])
    type = wtforms.TextField('Check Type', [wtforms.validators.Required()])
    data = wtforms.TextField('Data')
