#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/30 23:09
# @Author : LYX-夜光

from django import forms
from django.core.validators import RegexValidator

from djangoBackend.util.viewsTools import NewForm
from user.models import User

# 用户注册表单
class UserRegisterForm(NewForm):
    userName = forms.CharField(min_length=6,
                               max_length=30,
                               error_messages={
                                   'required': '用户名不能为空！',
                                   'min_length': '用户名不能少于6个字符！',
                                   'max_length': '用户名不能多于30个字符！',
                               },
                               validators=[RegexValidator(r'^[A-Za-z0-9_]+$', '用户名只能由字母、数字、下划线组成！')])
    password = forms.CharField(min_length=6,
                               max_length=16,
                               error_messages={
                                   'required': '密码不能为空！',
                                   'min_length': '密码不能少于6个字符！',
                                   'max_length': '密码不能多于16个字符！',
                               })
    email = forms.EmailField(error_messages={
                                 'required': '邮箱不能为空！',
                                 'invalid': '邮箱格式错误!',
                             })

    def clean_userName(self):
        userName = self.cleaned_data['userName']
        user = User.objects.filter(userName=userName).values('userId').first()
        if user:
            self.add_error('userName', forms.ValidationError('用户名已存在！'))
        return userName

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).values('userId').first()
        if user:
            self.add_error('email', forms.ValidationError('邮箱已被注册！'))
        return email

# 用户登录表单
class UserLoginForm(NewForm):
    loginName = forms.CharField(error_messages={'required': '用户名/邮箱不能为空！'})
    password = forms.CharField(error_messages={'required': '密码不能为空！'})