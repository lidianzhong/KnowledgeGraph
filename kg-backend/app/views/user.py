import re
from random import randint

from django.conf import settings
from django.core.cache import cache
import redis
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage

from app.utils.jsonResponse import json_response
from django.views.decorators.csrf import csrf_exempt
from app.models import User, Permission, UserPermission
import hashlib
from app.utils.jwtAuth import create_token

# 用户注册（完成）
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        verificationCode = request.POST.get('verificationCode')
        r = redis.Redis(host='127.0.0.1', port=6379)
        code_ = r.get(email)
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        def is_valid(testEmail):
            if re.fullmatch(regex, testEmail):
                return True
            else:
                return False
        if not is_valid(email):
            return json_response(213, '邮箱格式错误')
        if not (username and password and email and verificationCode):
            return json_response(201, '请输入完整数据')
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            print(username, email)
            return json_response(202, '账号或用户名已存在')
        if str(code_.decode()) != str(verificationCode):
            print(code_.decode(), verificationCode)
            return json_response(216, '验证码不正确或已失效')
        encry = hashlib.md5()
        encry.update(password.encode())
        md5_pwd = encry.hexdigest()  # 密码加密
        user = User(username=username, password=md5_pwd, email=email, role=0)
        user.save()
        # 导入权限表数据
        user_id = User.objects.filter(username=username).first()
        permission_list = Permission.objects.values_list("permission_id")
        for permission in permission_list:
            user_permission = UserPermission(user=user_id, permission_id=permission[0], is_allowed=0)
            user_permission.save()
        return json_response(200, '创建成功')
    else:
        return json_response(203, '无效的请求方法')


# 用户登录（完成）
@csrf_exempt
def login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        if not (password and email):
            return json_response(201, '请输入完整数据')
        if User.objects.filter(email=email):  # 账号存在
            encry = hashlib.md5()
            encry.update(password.encode())
            md5_pwd = encry.hexdigest()  # 密码加密
            user = User.objects.filter(email=email, password=md5_pwd).first()
            if user:
                token = create_token({"email": email})
                return json_response(200, '登录成功', {"username": user.username, "role": user.role, "token": token})
            else:
                return json_response(211, '密码错误')
        else:
            return json_response(205, '账号不存在')
    else:
        return json_response(203, '无效的请求方法')


# # 用户注销（改为前端实现）
# @csrf_exempt
# def logoff(request):
#     logout(request)
#     return json_response(200, '注销成功')

# 获取所有用户列表（分页显示）（需要管理员权限）
@csrf_exempt
def get_user_list(request):
    if request.method == 'GET':
        user = User.objects.filter(email=request.user_info).first()
        if user.role == 1:
            users = User.objects.all().values()

            # 此处使用 Django 自带的分页查询功能
            # 设置每页显示的记录数，这里假设一页显示10条记录
            items_per_page = request.GET.get('pageSize', 10)
            paginator = Paginator(users, items_per_page)

            # 获取URL参数中的页码，默认为第一页
            page_number = request.GET.get('page', 1)

            try:
                # 获取指定页码的数据
                current_page = paginator.page(page_number)
                # 将当前页的记录转换成列表
                current_page_data = list(current_page)
                # 获取分页信息
                pagination_info = {
                    'total_pages': paginator.num_pages,
                    'current_page': current_page.number,
                    'has_next': current_page.has_next(),
                    'has_previous': current_page.has_previous(),
                }
                # 构建响应数据
                response_data = {
                    'current_page_data': current_page_data,
                    'pagination': pagination_info,
                }
                return json_response(200, "第"+page_number+"页请求成功", response_data)
            except EmptyPage:
                # 如果指定的页码不存在，返回404错误
                return json_response(404, "页码不存在")
        else:
            return json_response(206, "该操作无权限")
    else:
        return json_response(203, "请求方式错误")

@csrf_exempt
def delete_self(request):
    if request.method == 'GET':
        user = User.objects.filter(email=request.user_info).first()
        if user is None:
            return json_response(205, "账号不存在")
        if user.role == 1:
            return json_response(212, "管理员不可注销自己")
        user.delete()
        return json_response(200, '操作成功')
    else:
        return json_response(203, "请求方式错误")

@csrf_exempt
def verification_code(request):
    if request.method == 'POST':
        # 从前端获取验证码
        email = request.POST.get('email')
        # 生成随机的验证码
        code = Email_Code()
        ret = '您的验证码是{}'.format(code)
        # 给邮箱发送验证码
        my_email = send_mail('激活验证', ret, settings.DEFAULT_FROM_EMAIL, [email])
        if not my_email == 1:
            return json_response(215, "邮件发送失败")
        key = email
        r = redis.Redis(host='127.0.0.1', port=6379)
        r.set(key, code, 300)
        return json_response(200, "邮件发送成功，有效期 5 分钟")


@csrf_exempt
def Email_Code():
    code_ = ''
    code_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    for k in range(5):
        code_ += code_str[randint(0, 35)]
    return code_

@csrf_exempt
def test(response):
    print(cache.get('rennen0929@gmail.com'))
    return json_response(200, "OK")