from functools import wraps
from flask_login import current_user
from flask import redirect, request

from chat_server import dao


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/auth')

        return f(*args, **kwargs)

    return check


def not_auth(f):
    @wraps(f)
    def check(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')

        return f(*args, **kwargs)

    return check
