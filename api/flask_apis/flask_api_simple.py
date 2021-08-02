# -*-coding:utf-8 -*-
"""
FileName: flask_api
Author: raphealwu
Date: 2021/2/7 10:23 下午
"""
import time

from flask import Flask, request
from api.token_utils.token_utils import toc


redis_host = 'localhost'
server = Flask(__name__)
user_info = "user_info"

# 用户数据
user_info_dict = {}
product_info_list = []
payload = {"api": "test"}


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
        return {"code": 400, "message": "用户名或密码不能为空"}
    if str(username) not in user_info_dict:
        user_info_dict[str(username)] = str(password)
        return {"code": 200, "message": "注册成功"}
    return {"code": 500, "message": "用户已注册，无需再次注册"}


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
        return {"code": 400, "message": "用户名或密码不能为空"}
    if str(username) in user_info_dict:
        return {"code": 200, "message": "登录成功", "token": toc.generate_token(payload)}
    else:
        return {"code": 401, "message": "用户还未注册，请先注册"}


# 产品创建接口
@server.route("/api/v1/create", methods=["POST"])
def create_products():
    """
    产品创建接口
    :return:
    """
    token = request.headers.get('token')
    if not token:
        return {"code": 401, "message": "无访问权限，拒绝访问"}
    username = request.form.get("username")
    product_name = request.form.get("productName")
    price = request.form.get("price")
    vendor = request.form.get("vendor")
    if not str(username) or not str(product_name) or not str(price) or not str(vendor):
        return {"code": 400, "message": "参数错误"}
    product_info = {"username": str(username), "productName": str(product_name), "price": price, "vendor": str(vendor)}
    product_info_list.append(product_info)
    return {"code": 200, "message": "产品新增成功"}


# 产品查询接口
@server.route("/api/v1/query", methods=["GET"])
def get_products_info():
    """
    产品创建接口
    :return:
    """
    token = request.headers.get('token')
    if not token:
        return {"code": 401, "message": "无访问权限，拒绝访问"}
    username = request.args.get("username")
    if not username:
        return {"code": 400, "message": "参数错误"}
    user_prod_query_info = []
    for _, item in enumerate(product_info_list):
        if item["username"] == username:
            user_prod_query_info.append(item)
    return {"code": 200, "message": "查询成功", "data": user_prod_query_info}


# 产品修改接口
@server.route("/api/v1/update", methods=["PUT"])
def modify_products_info():
    """
    产品修改接口
    :return:
    """
    token = request.headers.get('token')
    if not token:
        return {"code": 401, "message": "无访问权限，拒绝访问"}
    username = request.form.get("username")
    product_name = request.form.get("productName")
    price = request.form.get("price")
    vendor = request.form.get("vendor")

    if not str(username) or not str(product_name) or not str(price) or not str(vendor):
        return {"code": 400, "message": "参数错误"}

    for _, item in enumerate(product_info_list):
        if item["username"] == username:
            item["productName"] = str(product_name)
            item["price"] = price
            item["vendor"] = str(vendor)
            return {"code": 200, "message": "产品修改成功"}
    return {"code": 400, "message": "该用户没有商品，修改失败"}


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

    username = request.form.get("username")
    product_name = request.form.get("productName")
    price = request.form.get("price")
    vendor = request.form.get("vendor")
    for _, item in enumerate(product_info_list):
        if item["username"] == str(username) and item["productName"] == str(product_name) and item["price"] == price and item["vendor"] == str(vendor) :
            product_info_list.remove(item)
            return {"code": 200, "message": "删除成功"}
    return {"code": 500, "message": "删除错误"}


if __name__ == '__main__':
    server.run(debug=True)