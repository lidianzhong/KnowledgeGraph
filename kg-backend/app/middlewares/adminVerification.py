from app.utils.jsonResponse import json_response
from django.utils.deprecation import MiddlewareMixin
from app.models import User, Permission, UserPermission


# 中间件权限验证
class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url = request.get_full_path()
        black_list = ['permission']  # URL 以 permission 开头的都会进行权限验证
        if url.split('/')[1] in black_list:  # 该接口需进行权限验证
            email = request.user_info
            user = User.objects.filter(email=email).first()
            user_role = user.role
            if user_role == 0:  # 普通用户被阻止，管理员可放行
                return json_response(300, '无权限此操作')
