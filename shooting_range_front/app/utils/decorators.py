from flask import session

def scope_required(*role_names):
    def inner(func):
        def inner_inner(*args, **kwargs):
            user_roles = session['roles']
            for role_name in role_names:
                if role_name in user_roles:
                    return func(*args, **kwargs)
            return 'Forbidden access!', 403
        return inner_inner
    return inner
