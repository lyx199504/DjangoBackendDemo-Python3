#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/29 13:15
# @Author : LYX-夜光
from django.utils.deprecation import MiddlewareMixin

from djangoBackend.util.httpTools import RestResponse


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(str(exception))
        return RestResponse.serverFail()
