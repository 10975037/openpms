from functools import wraps
from flask import request, jsonify, current_app
import requests
import json


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        if 'X-Token' in request.headers:
            token = request.headers['X-Token']

        path = request.path
        method = request.method

        url = current_app.config['URL_PRIVILEGE_API']
        data = {
            'token': token,
            'app_id': current_app.config['APP_ID'],
            'path': path,
            'method': method
        }
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        result = r.json().get('data')
        if result:
            return func(*args, **kwargs)
        return jsonify({"code": 40000, "message": "无权访问"})
    return wrapper
