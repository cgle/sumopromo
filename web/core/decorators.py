from flask import request, redirect, url_for
from functools import wraps
from flask_login import current_user

from web import app

def demo_only(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        '''
            email: demo@sumo.promo
            password: demo
        '''
        if app.config['DEMO']:
            return redirect(url_for('account.login'))
        else:
            return f(*args, **kwargs)
    return decorated_func
