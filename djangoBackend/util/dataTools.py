#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/30 16:19
# @Author : LYX-夜光
import json

from django_redis import get_redis_connection

class RedisData:
    redisConn = get_redis_connection()

    @staticmethod  # 在redis中获取单个数据
    def getInfo(key, loads=True):
        try:
            results = RedisData.redisConn.get(key)
        except:
            results = None
        return results if not results or not loads else json.loads(results)

    @staticmethod  # 在redis中获取批量数据
    def getInfoList(keyList):
        try:
            redisConn = RedisData.redisConn.pipeline(transaction=False)
            for key in keyList:
                redisConn.get(key)
            results = redisConn.execute()
        except:
            results = []
        return results

    @staticmethod  # 在redis中设置信息， key键， results值， time设置时间（单位：s）
    def setInfo(key, results, time=-1, dumps=True):
        try:
            if dumps:
                RedisData.redisConn.set(key, json.dumps(results))
            else:
                RedisData.redisConn.set(key, results)
            if time > -1:
                RedisData.redisConn.expire(key, time)
            return True
        except:
            return False

    @staticmethod  # 在redis中批量设置信息， keyValue键值对， time设置时间（单位：s）
    def setInfoList(keyValue, time=-1, dumps=True):
        try:
            redisConn = RedisData.redisConn.pipeline(transaction=False)
            for key in keyValue:
                if dumps:
                    redisConn.set(key, json.dumps(keyValue[key]))
                else:
                    redisConn.set(key, keyValue[key])
                if time > -1:
                    redisConn.expire(key, time)
            redisConn.execute()
            return True
        except:
            return False

    @staticmethod  # 在redis中设置自增
    def setIncrease(key, amount=1, time=-1):
        try:
            RedisData.redisConn.incr(key, amount)
            if time > -1:
                RedisData.redisConn.expire(key, time)
            return True
        except:
            return False

    @staticmethod  # 设置redis键的有效时间
    def setTimeList(keyList, time):
        try:
            redisConn = RedisData.redisConn.pipeline(transaction=False)
            for key in keyList:
                redisConn.expire(key, time)
            redisConn.execute()
            return True
        except:
            return False