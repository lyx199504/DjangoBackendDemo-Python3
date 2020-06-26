#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/25 22:37
# @Author : LYX-夜光
from django.http import JsonResponse
from django.http.multipartparser import MultiPartParser


class HttpStatus:
    success = 200
    userError = 402
    serverError = 500

    @staticmethod  # 封装json接口
    def getResponse(code, msg, data):
        res = {'code': code, 'msg': msg, 'data': data}
        return JsonResponse(res)

class Fields:
    @staticmethod  # 获取一个model的属性字段
    def getOneField(field):
        return list(field.__dict__.values())[0].name

    @staticmethod  # 获取model的所有属性字段
    def getFields(model):
        return list(map(lambda field: field.name, model._meta.fields))

class Request:
    @staticmethod  # PUT请求获取body
    def body(request):
        return MultiPartParser(request.META, request, request.upload_handlers).parse()[0].dict()