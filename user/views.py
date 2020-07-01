
# Create your views here.
import datetime
import hashlib

from django.forms import model_to_dict
from django.http.multipartparser import MultiPartParser
from django.views import View

from djangoBackend.util.dataTools import Data
from djangoBackend.util.httpTools import RestResponse
from djangoBackend.util.tokenTools import Token
from user.forms import UserRegisterForm
from user.models import User

# 用户登录认证
class NewView(View):
    def setHeaders(self):
        self.device = self.request.META.get('HTTP_DEVICE', "")
        self.deviceId = self.request.META.get('HTTP_DEVICEID', "")
        if self.deviceId:
            self.deviceId = hashlib.md5(self.deviceId.encode('utf-8')).hexdigest()
        self.sn = self.request.META.get('HTTP_SN', "")

    def getPost(self):
        return self.request.POST.dict()

    def getPut(self):
        return MultiPartParser(self.request.META, self.request, self.request.upload_handlers).parse()[0].dict()

    # 用户认证
    def userAuth(self):
        self.setHeaders()
        self.userId = Token.validSn(self.sn, self.device, self.deviceId)
        if not self.userId:
            raise Exception('userAuthException')

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
        form = UserRegisterForm(self.getPost())
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

class UserSelfView(NewView):
    def get(self, request):
        self.userAuth()
        data = Data.getData(User, self.userId)
        return RestResponse.success("获取自己的信息成功！", data)

    def put(self, request):
        # PUT = Request.body(request)
        # field = ModelUnit.getOneField(User.userId)
        # isUpdate = User.objects.filter(userId=PUT[field]).update(**PUT)
        # if isUpdate:
        #     return RestResponse.success("修改成功！")
        return RestResponse.failure(RestResponse.USER_ERROR, "修改失败！")

class UserView(View):
    def get(self, request, userId):
        data = Data.getData(User, userId)
        return RestResponse.success("获取用户信息成功！", data)