
# Create your views here.
import datetime

from django import forms
from django.core.validators import RegexValidator
from django.forms import model_to_dict
from django.views import View

from djangoBackend.util.smallTools import RestResponse, ModelUnit, Request
from user.models import User


class UserRegisterForm(forms.Form):
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
    password2 = forms.CharField(error_messages={
                                   'required': '确认密码不能为空！',
                               })
    email = forms.EmailField(error_messages={
                                 'required': '邮箱不能为空！',
                                 'invalid': '邮箱格式错误!',
                             })

    def clean_userName(self):
        userNameValue = self.cleaned_data['userName']
        userId = ModelUnit.getOneFieldDB(User.userId)
        table = ModelUnit.getTableName(User)
        userName = ModelUnit.getOneFieldDB(User.userName)
        sql = "SELECT %s FROM %s WHERE %s=%s" % (userId, table, userName, '%s')
        results = User.objects.raw(sql, [userNameValue])
        if results:
            self.add_error('userName', forms.ValidationError('用户名已存在！'))
        return userNameValue

    def clean_email(self):
        emailValue = self.cleaned_data['email']
        userId = ModelUnit.getOneFieldDB(User.userId)
        table = ModelUnit.getTableName(User)
        email = ModelUnit.getOneFieldDB(User.email)
        sql = "SELECT %s FROM %s WHERE %s=%s" % (userId, table, email, '%s')
        results = User.objects.raw(sql, [emailValue])
        if results:
            self.add_error('email', forms.ValidationError('邮箱已被注册！'))
        return emailValue

    def clean(self):
        passwordValue = self.cleaned_data.get('password')
        password2Value = self.cleaned_data.get('password2')
        if not passwordValue or not password2Value:
            return self.cleaned_data
        if passwordValue != password2Value:
            self.add_error('password2', forms.ValidationError('二次输入密码不一致'))
        else:
            del self.cleaned_data['password2']
        return self.cleaned_data

class UserRegisterView(View):
    def post(self, request):
        form = UserRegisterForm(request.POST.dict())
        if not form.is_valid():
            errorDict = dict(form.errors)
            data = {key: errorDict[key][0] for key in errorDict}
            return RestResponse.failure(RestResponse.USER_ERROR, "注册失败！", data)
        user = form.cleaned_data
        user[ModelUnit.getOneField(User.nickname)] = user[ModelUnit.getOneField(User.userName)]
        now = datetime.datetime.now()
        user[ModelUnit.getOneField(User.birthday)] = now
        user[ModelUnit.getOneField(User.loginTime)] = now
        user[ModelUnit.getOneField(User.registerTime)] = now
        data = User.objects.create(**user)
        return RestResponse.success("注册成功！", {ModelUnit.getOneField(User.userId): data.userId})

class UsersView(View):
    def get(self, request):
        data = list(User.objects.all().values())
        return RestResponse.success("获取成功！", data)

    def put(self, request):
        PUT = Request.body(request)
        field = ModelUnit.getOneField(User.userId)
        isUpdate = User.objects.filter(userId=PUT[field]).update(**PUT)
        if isUpdate:
            return RestResponse.success("修改成功！")
        return RestResponse.failure(RestResponse.USER_ERROR, "修改失败！")

class UserView(View):
    def get(self, request, id):
        data = model_to_dict(User.objects.get(userId=id))
        return RestResponse.success("获取成功！", data)

    def delete(self, request, id):
        isDelete = User.objects.filter(userId=id).delete()
        if isDelete[0]:
            return RestResponse.success("删除成功！")
        return RestResponse.failure(RestResponse.USER_ERROR, "删除失败")