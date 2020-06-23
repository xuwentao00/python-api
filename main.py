#!flask/bin/python
# -- coding: utf-8 --

__author__ = 'cloudtogo'

from flask import Flask
from flask import request
import json
import hashlib
import time
app = Flask(__name__)

user_id = 1
USER = {}
token_user = {}
@app.route('/')
def index():
    return "hello world"

@app.route('/user/registry', methods=['POST'])
def registry():
    global USER
    global user_id
    global token_user
    try:
        body = request.get_json()
        account = body.get('account')
        password = body.get('password')
        if account and password:
            if len(password) < 6 and len(account)<2:
                result = {
                    "code": "error",
                    "message": "Your password or account is too short or does not meet other minimum requirements"
                }
                return json.dumps(result)
            if USER:
                if USER.get(account):
                    result = {
                        "code": "error",
                        "message": "The account has been registered"
                    }
                    return json.dumps(result)
                else:
                    m = hashlib.md5()
                    p = str(time.time()) + account + password
                    a = p.encode(encoding='utf-8')
                    m.update(a)
                    token = m.hexdigest()
                    ac = {
                        "account": account,
                        "user_id": user_id,
                        "password": password
                    }
                    USER[account] = ac
                    token_user[token] = ac
                    data = {
                        "code": 0,
                        "data": {
                            "token": token,
                            "user_id": user_id
                        },
                        "message": "Your registration was successful"
                    }
                    user_id = user_id + 1
                    return json.dumps(data)
            else:
                m = hashlib.md5()
                p = str(time.time()) + account + password
                a = p.encode(encoding='utf-8')
                m.update(a)
                token = m.hexdigest()
                ac = {
                        "account": account,
                        "token": token,
                        "user_id": user_id,
                        "password": password
                    }
                USER[account] = ac
                token_user[token] = ac
                data = {
                    "code": 0,
                    "data": {
                        "token": token,
                        "user_id": user_id
                    },
                    "message": "Your registration was successful"
                }
                user_id = user_id + 1
                return json.dumps(data)
    except Exception as e:
        err = {
            "code": "error",
            "message": "Argument error"
        }
        return json.dumps(err)


@app.route('/user/login', methods=['POST'])
def login():
    global USER
    global token_user
    try:
        body = request.get_json(silent=True)
        print(body)
        account = body.get("account")
        password = body.get("password")
        ac = USER.get(account)
        if ac:
            pwd = ac.get('password')
            if pwd == password:
                m = hashlib.md5()
                p = str(time.time()) + account + password
                a = p.encode(encoding='utf-8')
                m.update(a)
                token = m.hexdigest()
                token_user[token] = ac
                user_id = ac.get('user_id')
                data = {
                    "code": 0,
                    "data": {
                        "token": token,
                        "user_id": user_id
                    },
                    "message": "success"
                }
                return json.dumps(data)
        data = {
            "code": "error1",
            "message": "Account or password error"
        }
        return json.dumps(data)
    except Exception as e:
        err = {
            "code": "error2",
            "message": "Argument error"
        }
        return json.dumps(err)
# 添加/完善/查询个人信息
@app.route('/user', methods=['PUT', 'GET'])
def user():
    global token_user
    token = request.headers.get("token")
    method = request.method
    # 获取用户信息
    if method.upper() == 'GET':
        result = user_get(request)
        return result
    try:
        body = request.get_json(silent=True)
        name = body.get('name')
        age = body.get('age')
        phone = body.get('phone')
        """
        {
            "account": account,
            "token": token,
            "user_id": user_id,
            "password": password
        }
        """
        us = token_user.get(token)
        if us:
            us['age'] = age
            us['name'] = name
            us['phone'] = phone
            token_user[token] = us
            data = {
                "code": 0,
                "message": "success"
            }
            return json.dumps(data)
        else:
            err = {
                "code": "0",
                "data": {}
            }
            return json.dumps(err)

    except:
        err = {
            "code": "error",
            "message": "Argument Error"
        }
        return json.dumps(err)

# @app.route('/user', methods=['GET'])
def user_get(re):
    global token_user
    token = re.headers.get("token")
    try:
        re = token_user.get(token)
        if re:
            return re
        else:
            data={
                "code": 0,
                "data":{}
            }
    except:
        data = {
            "code": "error",
            "message": "Miss authorization information"
        }
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
