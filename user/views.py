
# Create your views here.
import datetime
import hashlib

from django.db.models import Q
from django.views import View

from djangoBackend.util.dataTools import Data
from djangoBackend.util.httpTools import RestResponse
from djangoBackend.util.tokenTools import Token
from djangoBackend.util.viewsTools import NewView
from user.forms import UserRegisterForm, UserLoginForm
from user.models import User

# 用户登录验证
class UserRegisterValidView(View):
    def post(self, request):
        form = UserRegisterForm(request.POST.dict())
        if not form.is_valid():
            return RestResponse.userFail("注册验证失败！", form.errorsDict())
        return RestResponse.success("注册验证成功！")

# 用户注册
class UserRegisterView(NewView):
    def post(self, request):
        self.setHeaders()
        form = UserRegisterForm(self.getPost())
        if not form.is_valid():
            return RestResponse.userFail("注册失败！", form.errorsDict())
        user = form.cleaned_data
        user['password'] = hashlib.md5(user['password'].encode()).hexdigest()
        user['nickname'] = user['userName']
        user['birthday'] = user['loginTime'] = user['registerTime'] = datetime.datetime.now()
        user = User.objects.create(**user)
        sn = Token.setSn(user.userId, self.device, self.deviceId)
        return RestResponse.success("注册成功！", {'userId': user.userId, 'sn': sn})

# 用户登录
class UserLoginView(NewView):
    def post(self, request):
        self.setHeaders()
        form = UserLoginForm(self.getPost())
        if not form.is_valid():
            return RestResponse.userFail("登录失败！", form.errorsDict())
        user = form.cleaned_data
        data = User.objects.filter(Q(userName=user['loginName']) | Q(email=user['loginName'])).values('userId').first()
        if not data:
            return RestResponse.userFail("登录名或密码错误！")
        sn = Token.setSn(data['userId'], self.device, self.deviceId)
        data['loginTime'] = datetime.datetime.now()
        Data.updateData(User, data)
        return RestResponse.success("登录成功！", {'userId': data['userId'], 'sn': sn})

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