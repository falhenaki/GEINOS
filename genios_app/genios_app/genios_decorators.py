from functools import wraps
from flask import request, redirect, url_for, session, render_template

def login_required(f):
    """
    Decorator that will check if user is logged in before following a route. If they are not logged in it will
    redirect them to the login page
    :param f: Input arguments
    :return: wrapped function that checks if user is logged in and if not will redirect to login page
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'username' in session:
            return render_template('login.html')
        return f(*args, **kwargs)
    return decorated_function

def has_permissions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if False:
            return redirect(url_for('permission_denied'))
        return f(*args, **kwargs)
    return decorated_function