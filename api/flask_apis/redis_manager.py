# -*-coding:utf-8 -*-
"""
FileName: redis_manager
Author: raphealwu
Date: 2021/2/7 9:44 下午
"""
from redis import StrictRedis


class RedisDBManager(object):
    """
    redis数据库操作
    """
    def __init__(self, host):
        self._host = host
        self.db_connect = None

    def __enter__(self):
        self.db_connect = StrictRedis(host=self._host, port=6379, db=0)
        return self.db_connect

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db_connect:
            self.db_connect.close()



