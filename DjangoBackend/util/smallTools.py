#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/25 22:37
# @Author : LYX-夜光
from django.http import JsonResponse
from django.http.multipartparser import MultiPartParser


class HttpResponse:
    SUCCESS = 200
    USER_ERROR = 402
    SERVER_ERROR = 500

    @staticmethod  # 封装json接口
    def success(msg="", data=None):
        return JsonResponse({'code': HttpResponse.SUCCESS, 'msg': msg, 'data': data})

    @staticmethod
    def failure(code, msg=""):
        return JsonResponse({'code': code, 'msg': msg, 'data': None})

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