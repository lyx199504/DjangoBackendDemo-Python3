
# Create your views here.
from django.forms import model_to_dict
from django.views import View

from djangoBackend.util.smallTools import HttpResponse, Fields, Request
from user.models import User

class UsersView(View):
    def get(self, request):
        data = list(User.objects.all().values())
        return HttpResponse.success("获取成功！", data)

    def post(self, request):
        try:
            data = User.objects.create(**request.POST.dict())
            field = Fields.getOneField(User.userId)
            return HttpResponse.success("添加成功！", {field: data.userId})
        except:
            return HttpResponse.failure(HttpResponse.SERVER_ERROR, "添加失败！服务器错误！")

    def put(self, request):
        try:
            PUT = Request.body(request)
            field = Fields.getOneField(User.userId)
            isUpdate = User.objects.filter(userId=PUT[field]).update(**PUT)
            if isUpdate:
                return HttpResponse.success("修改成功！")
            return HttpResponse.failure(HttpResponse.USER_ERROR, "修改失败！")
        except:
            return HttpResponse.failure(HttpResponse.SERVER_ERROR, "服务器错误！")

class UserView(View):
    def get(self, request, id):
        try:
            data = model_to_dict(User.objects.get(userId=id))
            return HttpResponse.success("获取成功！", data)
        except:
            return HttpResponse.failure(HttpResponse.USER_ERROR, "获取失败")

    def delete(self, request, id):
        isDelete = User.objects.filter(userId=id).delete()
        if isDelete[0]:
            return HttpResponse.success("删除成功！")
        return HttpResponse.failure(HttpResponse.USER_ERROR, "删除失败")