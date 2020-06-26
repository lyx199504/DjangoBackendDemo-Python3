
# Create your views here.
from django.forms import model_to_dict
from django.views import View

from DjangoBackend.util.smallTools import HttpStatus, Fields, Request
from user.models import User

class UsersView(View):
    def get(self, request):
        data = list(User.objects.all().values())
        return HttpStatus.getResponse(HttpStatus.success, "获取成功！", data)

    def post(self, request):
        try:
            data = User.objects.create(**request.POST.dict())
            field = Fields.getOneField(User.userId)
            return HttpStatus.getResponse(HttpStatus.success, "添加成功！", {field: data.userId})
        except:
            return HttpStatus.getResponse(HttpStatus.serverError, "添加失败！服务器错误！", None)

    def put(self, request):
        try:
            PUT = Request.body(request)
            field = Fields.getOneField(User.userId)
            isUpdate = User.objects.filter(userId=PUT[field]).update(**PUT)
            if isUpdate:
                return HttpStatus.getResponse(HttpStatus.success, "修改成功！", None)
            return HttpStatus.getResponse(HttpStatus.userError, "修改失败！", None)
        except:
            return HttpStatus.getResponse(HttpStatus.serverError, "服务器错误！", None)

class UserView(View):
    def get(self, request, id):
        try:
            data = model_to_dict(User.objects.get(userId=id))
            return HttpStatus.getResponse(HttpStatus.success, "获取成功！", data)
        except:
            return HttpStatus.getResponse(HttpStatus.userError, "获取失败", None)

    def delete(self, request, id):
        isDelete = User.objects.filter(userId=id).delete()
        if isDelete[0]:
            return HttpStatus.getResponse(HttpStatus.success, "删除成功！", None)
        return HttpStatus.getResponse(HttpStatus.userError, "删除失败", None)