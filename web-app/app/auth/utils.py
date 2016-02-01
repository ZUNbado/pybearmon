from flask.ext.login import current_user

def user_logged():
    return not current_user.is_anonymous

def user_anonymous():
    return current_user.is_anonymous

def user_admin():
    return current_user.is_admin()
