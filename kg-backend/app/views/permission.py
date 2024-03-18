from django.views.decorators.csrf import csrf_exempt
from app.utils.jsonResponse import json_response
from app.models import User, UserPermission
import json


# 查询某一用户对应权限
@csrf_exempt
def get_user_permission(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        user_permission = UserPermission.objects.filter(user=user_id)
        if user_permission.first() is None:
            return json_response(204, '该用户不存在')
        else:
            return json_response(200, '权限查询成功', list(user_permission.values()))
    else:
        return json_response(203, '请求方式错误')


# 修改用户权限
@csrf_exempt
def change_permission(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        permission_id = [int(num) for num in request.POST.get('permission_id').split(",")]
        is_allowed = [int(num) for num in request.POST.get('is_allowed').split(",")]
        print(user_id, permission_id, is_allowed)
        for i in range(len(permission_id)):
            userpermission = UserPermission.objects.filter(user_id=user_id, permission_id=permission_id[i]).first()
            userpermission.is_allowed = is_allowed[i]
            userpermission.save()
        return json_response(200, '修改成功')
    else:
        return json_response(203, '请求方式错误')


# 授予管理员权限
@csrf_exempt
def grant_admin(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_admin = User.objects.filter(user_id=user_id).first()
        new_admin.role = 1
        new_admin.save()
        userpermission = UserPermission.objects.filter(user_id=user_id)
        userpermission.delete()
        return json_response(200, '操作成功')
    else:
        return json_response(203, '请求方式错误')


# 删除用户
@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_del = User.objects.filter(user_id=user_id).first()
        if user_del is None:
            return json_response(204, '该用户不存在')
        user_del.delete()
        return json_response(200, '操作成功')
    else:
        return json_response(203, '请求方式错误')
