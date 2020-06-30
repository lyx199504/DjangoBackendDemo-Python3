
# Create your views here.
import datetime
import hashlib

from django.forms import model_to_dict
from django.http.multipartparser import MultiPartParser
from django.views import View

from djangoBackend.util.httpTools import RestResponse
from djangoBackend.util.userTools import Token
from user.forms import UserRegisterForm
from user.models import User

# 用户登录认证
class NewView(View):
    def setHeaders(self):
        self.device = self.request.META.get('HTTP_DEVICE', "")
        self.deviceId = self.request.META.get('HTTP_DEVICEID', "")
        self.sn = self.request.META.get('HTTP_SN', "")

    def getPost(self):
        return self.request.POST.dict()

    def getPut(self):
        return MultiPartParser(self.request.META, self.request, self.request.upload_handlers).parse()[0].dict()

    def userAuth(self):
        self.setHeaders()
        self.deviceId = hashlib.md5(self.deviceId.encode('utf-8')).hexdigest()
        self.userId = Token.validSn(self.sn, self.device, self.deviceId)  # 用户认证

# 用户登录验证
class UserRegisterValidView(View):
    def post(self, request):
        form = UserRegisterForm(request.POST.dict())
        if not form.is_valid():
            errorDict = dict(form.errors)
            errorDict = {key: errorDict[key][0] for key in errorDict}
            return RestResponse.userFail("验证失败！", errorDict)
        return RestResponse.success("验证成功！")

# 用户注册
class UserRegisterView(NewView):
    def post(self, request):
        self.setHeaders()
        form = UserRegisterForm(request.POST.dict())
        if not form.is_valid():
            errorDict = dict(form.errors)
            errorDict = {key: errorDict[key][0] for key in errorDict}
            return RestResponse.userFail("注册失败！", errorDict)
        user = form.cleaned_data
        user['password'] = hashlib.md5(user['password'].encode()).hexdigest()
        user['nickname'] = user['userName']
        user['birthday'] = user['loginTime'] = user['registerTime'] = datetime.datetime.now()
        user = User.objects.create(**user)
        sn = Token.setSn(user.userId, self.device, self.deviceId)
        return RestResponse.success("注册成功！", {'userId': user.userId, 'sn': sn})



# 用户登录
class UserLoginView(View):
    def post(self, request):
        return RestResponse.success("登录成功！")

class UsersView(View):
    def get(self, request):
        data = list(User.objects.all().values())
        return RestResponse.success("获取成功！", data)

    def put(self, request):
        # PUT = Request.body(request)
        # field = ModelUnit.getOneField(User.userId)
        # isUpdate = User.objects.filter(userId=PUT[field]).update(**PUT)
        # if isUpdate:
        #     return RestResponse.success("修改成功！")
        return RestResponse.failure(RestResponse.USER_ERROR, "修改失败！")

class UserView(View):
    def get(self, request, userId):
        user = User.objects.get(userId=userId)
        print(user)
        if not user:
            return RestResponse.userFail("获取失败！")
        data = model_to_dict(user)
        return RestResponse.success("获取成功！", data)

    def delete(self, request, userId):
        isDelete = User.objects.filter(userId=userId).delete()
        if isDelete[0]:
            return RestResponse.success("删除成功！")
        return RestResponse.failure(RestResponse.USER_ERROR, "删除失败")