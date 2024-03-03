from app.utils.jsonResponse import json_response
from django.utils.deprecation import MiddlewareMixin
from app.models import User, Permission, UserPermission


# 中间件权限验证
class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url = request.get_full_path()
        black_list = ['/file/changeFile', '/file/deleteFile', '/answer/changeAnswer', '/answer/deleteAnswer']
        if url in black_list:  # 该接口需进行权限验证
            print("测试权限验证")
            email = request.user_info
            permission_name = url.split('/')[2]
            user = User.objects.filter(email=email).first()
            user_role = user.role
            print(user_role)

            if user_role == 0:  # 普通用户需要检查对应的权限，管理员可放行
                user_id = user.user_id

                print(user_id,  permission_name)
                permission = Permission.objects.filter(permission_name=permission_name).first()
                permission_id = permission.permission_id
                is_allowed = UserPermission.objects.filter(user_id=user_id, permission_id=permission_id).values(
                    "is_allowed").first()['is_allowed']
                print(permission_id, user_id, email, permission_name)
                if is_allowed == 0:
                    return json_response(206, '无权限此操作')
