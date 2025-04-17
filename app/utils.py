from flask import request, current_app

def get_username():
    ip = request.remote_addr
    return current_app.config['USERS'].get(ip)

def is_authorized():
    return get_username() is not None
