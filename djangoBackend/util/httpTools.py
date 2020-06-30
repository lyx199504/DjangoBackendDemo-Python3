#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/25 22:37
# @Author : LYX-夜光
from django.http import JsonResponse


class RestResponse:
    SUCCESS = 200
    AUTH_ERROR = 401
    USER_ERROR = 402
    SERVER_ERROR = 500

    @staticmethod  # 封装json接口
    def success(msg='', data=None):
        return JsonResponse({'code': RestResponse.SUCCESS, 'msg': msg, 'data': data})

    @staticmethod
    def failure(code, msg='', data=None):
        return JsonResponse({'code': code, 'msg': msg, 'data': data})

    @staticmethod
    def userFail(msg='', data=None):
        return JsonResponse({'code': RestResponse.USER_ERROR, 'msg': msg, 'data': data})

    @staticmethod
    def serverFail():
        return JsonResponse({'code': RestResponse.SERVER_ERROR, 'msg': '服务器错误！', 'data': None})