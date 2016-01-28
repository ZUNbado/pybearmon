from flask.ext.login import current_user

def user_logged():
    return current_user.is_active()

def user_anonymous():
    return not current_user.is_active()
