# -*-coding:utf-8 -*-
"""
FileName: flask_api
Author: raphealwu
Date: 2021/2/7 10:23 下午
"""
from flask import Flask, request
from api.token_utils.token_utils import  toc
from api.flask_apis.redis_manager import RedisDBManager


redis_host = 'localhost'
server = Flask(__name__)
user_info = "user_info"


# 注册接口
@server.route("/api/v1/register", methods=["POST"])
def register():
    """
    注册接口，使用用户名和密码
    :return:
    """
    username = request.form.get("username")
    password = request.form.get("password")
    if not str(username) or not str(password):
        return {"code": 500, "message": "用户名或密码不能为空"}
    with RedisDBManager(redis_host) as r:
        if bytes.decode(r.hget(user_info, str(username))) == str(password):
            return {"code": 401, "message": "用户已经注册，无需再次注册"}
        r.hset(user_info, str(username), str(password).encode('utf-8'))
        print(r.hget(user_info, username))
    return {"code": 200, "message": "注册成功"}


# 登陆接口
@server.route("/api/v1/login", methods=["POST"])
def login():
    """
    登陆接口，使用用户名和密码
    :return:
    """
    username = request.form.get("username")
    password = request.form.get("password")
    if not str(username) or not str(password):
        return {"code": 500, "message": "用户名或密码不能为空"}
    with RedisDBManager(redis_host) as r:
        if bytes.decode(r.hget(user_info, str(username))) == str(password):
            token = toc.generate_token()
            return {"code": 200, "message": "登陆成功", "token": token}
        else:
            return {"code": 401, "message": "用户还没有注册，请先注册"}


if __name__ == '__main__':
    server.run(debug=True)




