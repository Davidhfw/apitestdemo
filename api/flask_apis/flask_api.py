# -*-coding:utf-8 -*-
"""
FileName: flask_api
Author: raphealwu
Date: 2021/2/7 10:23 下午
"""
import time

from flask import Flask, request
from api.token_utils.token_utils import toc
from api.flask_apis.redis_manager import RedisDBManager
import logging


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
        if r.hexists(user_info, str(username)):
            if bytes.decode(r.hget(user_info, str(username))) == str(password):
                return {"code": 401, "message": "用户已经注册，无需再次注册"}
        r.hset(user_info, username, password)
        logging.info(r.hget(user_info, username))
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
        logging.info(r.hget(user_info, username))
        if r.hexists(user_info, username):
            logging.info(bytes.decode(r.hget(user_info, username)))
            if bytes.decode(r.hget(user_info, username)) == password:
                return {"code": 200, "message": "登陆成功", "token": toc.generate_token()}
            else:
                return {"code": 500, "message": "用户名或密码不存在"}
        else:
            return {"code": 401, "message": "用户还没有注册，请先注册"}


# 产品创建接口
@server.route("/api/v1/createProd", methods=["POST"])
def create_products():
    """
    产品创建接口
    :return:
    """
    token = request.headers.get('token')
    if not token:
        return {"code": 401, "message": "无访问权限，拒绝访问"}
    if not toc.verify_token(token):
        return {"code": 401, "message": "token失效，请重新获取"}
    username = request.form.get("username")
    product_name = request.form.get("productName")
    price = request.form.get("price")
    vendor = request.form.get("vendor")

    with RedisDBManager(redis_host) as r:
        if r.hexists(user_info, username):
            products_info = {f"{username}": f"{product_name}-{price}-{vendor}"}
            if r.hexists("products_info", username):
                if bytes.decode(r.hget("products_info", username)) == f"{product_name}-{price}-{vendor}":
                    return {"code": 500, "message": "产品信息已经存在，新增产品失败"}
            else:
                r.hmset("products_info", products_info)
                return {"code": 200, "message": "新增产品成功"}
        else:
            return {"code": 500, "message": "用户信息不存在"}


# 产品查询接口
@server.route("/api/v1/queryProds", methods=["GET"])
def get_products_info():
    """
    产品创建接口
    :return:
    """
    token = request.headers.get('token')
    if not token:
        return {"code": 401, "message": "无访问权限，拒绝访问"}
    # if not toc.verify_token(token):
    #     return {"code": 401, "message": "token失效，请重新获取"}
    username = request.args.get("username")
    if not username:
        return {"code": 500, "message": "用户名不能为空"}
    with RedisDBManager(redis_host) as r:
        if r.hexists("products_info", username):
            data = bytes.decode(r.hget("products_info", username))
            return {"code": 200, "message": "查询成功", "data": data}
        else:
            return {"code": 500, "message": "用户信息不存在"}


# 产品修改接口
@server.route("/api/v1/modify", methods=["PUT"])
def modify_products_info():
    """
    产品修改接口
    :return:
    """
    token = request.headers.get('token')
    if not token:
        return {"code": 401, "message": "无访问权限，拒绝访问"}
    # if not toc.verify_token(token):
    #     return {"code": 401, "message": "token失效，请重新获取"}
    username = request.form.get("username")
    product_name = request.form.get("productName")
    price = request.form.get("price")
    vendor = request.form.get("vendor")

    with RedisDBManager(redis_host) as r:
        if bytes.decode(r.hget(user_info, str(username))):
            products_info = {f"{username}": f"{product_name}-{price}-{vendor}"}
            r.hmset("products_info", products_info)
            return {"code": 200, "message": "产品修改成功"}


# 产品删除接口
@server.route("/api/v1/delete", methods=["DELETE"])
def delete_products_info():
    """
    产品删除接口
    :return:
    """
    token = request.headers.get('token')
    if not token:
        return {"code": 401, "message": "无访问权限，拒绝访问"}
    # if not toc.verify_token(token):
    #     return {"code": 401, "message": "token失效，请重新获取"}
    username = request.form.get("username")
    with RedisDBManager(redis_host) as r:
        if bytes.decode(r.hget(user_info, str(username))):
            r.hdel("products_info", username)
            return {"code": 200, "message": "产品删除成功"}
        else:
            return {"code": 500, "message": "产品不存在或者已经被删除"}


if __name__ == '__main__':
    server.run(debug=True)




