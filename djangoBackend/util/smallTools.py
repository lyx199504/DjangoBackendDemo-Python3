#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/25 22:37
# @Author : LYX-夜光
from django.http import JsonResponse
from django.http.multipartparser import MultiPartParser


class RestResponse:
    SUCCESS = 200
    AUTH_ERROR = 401
    USER_ERROR = 402
    SERVER_ERROR = 500

    @staticmethod  # 封装json接口
    def success(msg="", data=None):
        return JsonResponse({'code': RestResponse.SUCCESS, 'msg': msg, 'data': data})

    @staticmethod
    def failure(code, msg="", data=None):
        return JsonResponse({'code': code, 'msg': msg, 'data': data})

class ModelUnit:
    @staticmethod  # 获取数据表名
    def getTableName(model):
        return model._meta.db_table

    @staticmethod  # 获取一个数据表字段
    def getOneFieldDB(field):
        return list(field.__dict__.values())[0].column

    @staticmethod  # 获取一个model属性
    def getOneField(field):
        return list(field.__dict__.values())[0].name

    @staticmethod  # 获取多个model属性
    def getManyFields(fields):
        return [list(field.__dict__.values())[0].name for field in fields]

    @staticmethod  # 获取所有model属性
    def getAllFields(model):
        return list(map(lambda field: field.name, model._meta.fields))

class Request:
    @staticmethod  # PUT请求获取body
    def body(request):
        return MultiPartParser(request.META, request, request.upload_handlers).parse()[0].dict()