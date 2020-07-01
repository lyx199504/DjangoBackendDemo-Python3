#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/17 14:27
# @Author : snowmusic

import time
import random
import hashlib
import base64

from djangoBackend.util.dataTools import RedisData

class Token:
    REDIS_TIME = 60*60*24*7  # 7天

    # DBJ2 Hash算法
    def DBJHash(self, strValue):
        hashValue = 6359  # 稍微大的素数即可，比如：5381
        for char in strValue:
            hashValue = (((hashValue << 5) + hashValue) + ord(char)) & 0xffffffff
        return hashValue

    # token认证，生成sn
    def encodeSn(self, id, device, deviceId):
        prefixCode = self.DBJHash(device + deviceId)  # 用系统和设备id作为前缀码
        originStr = device + deviceId + str(time.time()) + str(random.random())  # 原始串
        originHash = hashlib.md5(originStr.encode('utf-8')).hexdigest()[16:]  # 哈希串
        idCode = (self.DBJHash(originHash) | prefixCode) ^ id  # id编码加密，异或是为了可以在解密时通过id编码拿到id
        pieceStr = originHash + "_" + str(idCode)  # 哈希串和id编码拼接
        pieceStrMap = str(((self.DBJHash(pieceStr) ^ 5381) & 0xffff) % 10000)  # 映射
        linkStr = pieceStr + "/" + pieceStrMap
        return base64.b64encode(linkStr.encode('utf-8')).decode()  # base64编码为sn

    # 解码sn，获取id，encodeSn的逆算法
    def decodeSn(self, sn, device, deviceId):
        try:
            prefixCode = self.DBJHash(device + deviceId)
            pieceStrList = base64.b64decode(sn.encode('utf-8')).decode().split("/")
            if len(pieceStrList) != 2:
                return None
            pieceStr, pieceStrMap = pieceStrList
            if pieceStrMap != str(((self.DBJHash(pieceStr) ^ 5381) & 0xffff) % 10000):
                return None
            splitList = pieceStr.split("_")
            if len(splitList) != 2:
                return None
            originHash, idCode = splitList
            id = (self.DBJHash(originHash) | prefixCode) ^ int(idCode)
            return id
        except:
            return None

    # 根据id在redis中获取sn
    def getSn(self, id, device):
        key = RedisData.getSnKey(id, device)
        return RedisData.getData(key)

    @staticmethod  # 验证sn
    def validSn(sn, device, deviceId):
        token = Token()
        id = token.decodeSn(sn, device, deviceId)
        if id:
            sn_redis = token.getSn(id, device)
            if sn_redis == sn:
                return id
        return None

    @staticmethod  # 将sn与id分别存入redis
    def setSn(id, device, deviceId):
        token = Token()
        key = RedisData.getSnKey(id, device)
        sn = token.encodeSn(id, device, deviceId)
        success = RedisData.setData(key, sn, Token.REDIS_TIME)
        return sn if success else ""
