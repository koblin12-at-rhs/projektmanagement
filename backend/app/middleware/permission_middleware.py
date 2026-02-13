from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            abort(403, description="Admin permissions required")
        return func(*args, **kwargs)

    return wrapped
