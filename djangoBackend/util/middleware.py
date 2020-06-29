#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/29 13:15
# @Author : LYX-夜光
from django.utils.deprecation import MiddlewareMixin

from djangoBackend.util.smallTools import RestResponse


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(str(exception))
        return RestResponse.failure(RestResponse.SERVER_ERROR, "服务器错误！")
