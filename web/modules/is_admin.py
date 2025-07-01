from flask import render_template
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return render_template('erros/403.html'), 403
        return f(*
                 args, **kwargs)
    return wrapper
