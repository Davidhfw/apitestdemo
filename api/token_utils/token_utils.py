# -*-coding:utf-8 -*-
"""
FileName: token_utils
Author: raphealwu
Date: 2021/2/7 9:21 下午
"""
import time

import jwt


class TokenUtils(object):
    """
    jwt token utils class
    """
    def __init__(self):
        self._algo = 'H256'
        self._secret = 'api-test-demo'
        self._expire = 7200
        self._payload = None

    @property
    def algo(self):
        return self._algo

    @algo.setter
    def algo(self, value):
        if not isinstance(value, str):
            raise ValueError('algo must be string')
        if value == '':
            raise ValueError("algo must not be null string")
        else:
            self._algo = value

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, value):
        if not isinstance(value, str):
            raise ValueError("secret should be string")
        if value != '':
            self._secret = value
        else:
            raise ValueError("secret should not be null str")

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        if self._payload is None:
            self._payload = {
                "iat": time.time(),
                "exp": time.time() + self._expire
            }
        else:
            if not isinstance(value, dict):
                raise ValueError("payload must be dict")
            self._payload = value

    @property
    def expire(self):
        return self._expire

    @expire.setter
    def expire(self, value):
        if not isinstance(value, int):
            raise ValueError("expire must be integer")
        if 0 > value > 7200:
            raise ValueError("expire value must be between 1 and 7200")
        else:
            self._expire = value

    def generate_token(self):
        # 生成token
        try:
            token = jwt.encode(self._payload, self._secret, algorithm=self._algo)
        except Exception as e:
            raise e
        else:
            return token

    def parse_token(self, token):
        # 解析token中的payload
        try:
            data = jwt.decode(token, self._secret, algorithms=[self._algo])
        except Exception as e:
            raise e
        else:
            return data

    def verify_token(self, token):
        # 验证token是否有效，有效返回为True, 反之返回False
        return self.parse_token(token) == self._payload


toc = TokenUtils()