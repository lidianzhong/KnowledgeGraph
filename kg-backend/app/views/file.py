import asyncio
import subprocess

from celery import shared_task
from django.views.decorators.csrf import csrf_exempt

from app.utils.callModel import call_model
from app.utils.jsonResponse import json_response
from app.models import Document, User, QApair
import time
from datetime import datetime
from django.http import QueryDict
from django.core.paginator import Paginator, EmptyPage



# 上传文献，有权限控制（开发中，测试中）
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        # =============== 解析请求参数 ===============
        title = request.POST.get('title')
        content = request.POST.get('content')
        # =============== 获取token信息 ===============
        user_email = request.user_info
        # =============== 获取数据库信息 ===============
        user = User.objects.filter(email=user_email).first()
        # =============== 保存到本地数据库 ===============
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间戳
        update_time = create_time
        user_name = user.username
        file = Document(create_time=create_time, update_time=update_time, title=title,
                        content=content, user_name=user_name)
        file.save()
        
        # ============ 调用服务器模型返回 QA List ============
        json_response(200, '文献提交成功')
        qa_list = call_model(content)
        for qa in qa_list:
            qa_pair = QApair(question=qa['question'], answer=qa['answer'], document_id=file.pk)
            qa_pair.save()

        return json_response(200, '上传成功，模型正在调用，稍后会生成问答对和知识图谱')
    else:
        return json_response(203, '请求方式错误')


# # 搜索文献（开发中）
# @csrf_exempt
# def search_file_list(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         page = int(request.POST.get('currentPage'))
#         page_size = int(request.POST.get('pageSize'))
#
#         email = request.user_info
#         user_id = User.objects.filter(email=email).first().user_id
#         # 模糊查询
#         file_list = Document.objects.filter(title__contains=title, user=user_id).values()
#         start = (page - 1) * page_size
#         end = page * page_size
#         file_list = file_list[start:end]
#         total = len(Document.objects.filter(title__contains=title, user=user_id))
#         files = []
#         for file in file_list:
#             file_dict = {}  # 必须放在循环内部
#             file_dict['document_id'] = file['document_id']
#             file_dict['title'] = file['title']
#             files.append(file_dict)
#         data = {'data': files, 'total': total}
#         return json_response(200, '请求成功', data)
#     else:
#         return json_response(203, '请求方式错误')


# 获取某个文献详细内容，无权限控制(下载文献)
@csrf_exempt
def get_file_detail(request):
    if request.method == 'GET':
        document_id = request.GET.get('document_id')
        if Document.objects.filter(document_id=document_id).exists():
            document = Document.objects.filter(document_id=document_id).first()
            file_dict = {'document_id': document.document_id,
                         'title': document.title,
                         'create_time': document.create_time,
                         'update_time': document.update_time,
                         'content': document.content,
                         'user_name': document.user_name}
            return json_response(200, '请求成功', file_dict)
        else:
            return json_response(215, '该文献不存在')

    else:
        return json_response(203, '请求方式错误')


# # 获取已通过审核的文献列表，无权限控制
# @csrf_exempt
# def get_success_files(request):
#     if request.method == 'POST':
#         user_id = User.objects.filter(email=request.user_info).first().user_id
#         files = Document.objects.select_related('auditor').all().filter(user=user_id, status=1).order_by('-create_time')
#         # 设置分页
#         total = files.count()
#         page = int(request.POST.get('currentpage'))
#         page_size = int(request.POST.get('pageSize'))
#         start = (page - 1) * page_size
#         end = page * page_size
#         files = files[start:end]
#         file_list = []
#         for file in files:
#             file_dict = {}
#             file_dict['document_id'] = file.document_id
#             file_dict['field'] = file.field.field_name
#             file_dict['title'] = file.title
#             file_dict['create_time'] = file.create_time
#             # file_dict['update_time'] = file.update_time
#             file_list.append(file_dict)
#         data = {'data': file_list, 'total': total}
#         return json_response(200, '请求成功', data)
#     else:
#         return json_response(203, '请求方式错误')


# 获取未通过审核的文献列表，无权限控制
# @csrf_exempt
# def get_failure_files(request):
#     if request.method == 'GET':
#         user_id = User.objects.filter(email=request.user_info).first().user_id
#         files = Document.objects.select_related('auditor').all().filter(user=user_id, status=2)
#         file_list = []
#         for file in files:
#             file_dict = {}
#             file_dict['document_id'] = file.document_id
#             file_dict['field'] = file.field
#             file_dict['title'] = file.title
#             file_dict['create_time'] = file.create_time
#             file_dict['update_time'] = file.update_time
#             file_dict['status'] = file.status
#             file_dict['content'] = file.content
#             file_dict['reason'] = file.reason
#             file_dict['author'] = file.auditor.username
#             file_list.append(file_dict)
#         return json_response(200, '请求成功', file_list)
#     else:
#         return json_response(203, '请求方式错误')

# # 获取所有文献列表，无权限控制
# @csrf_exempt
# def get_all_files(request):
#     if request.method == 'GET':
#         user_id = User.objects.filter(email=request.user_info).first().user_id
#         files = Document.objects.filter(user=user_id).values()
#         return json_response(200, '请求成功', list(files))
#     else:
#         return json_response(203, '请求方式错误')

# 查询所有文献（分页）（测试中）
@csrf_exempt
def get_all_files(request):
    if request.method == 'GET':
        files = Document.objects.all().values().order_by('-create_time')

        # 此处使用 Django 自带的分页查询功能
        # 设置每页显示的记录数，这里假设一页显示10条记录
        items_per_page = request.GET.get('pageSize', 5)
        paginator = Paginator(files, items_per_page)

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
            return json_response(200, "请求成功", response_data)
        except EmptyPage:
            # 如果指定的页码不存在，返回404错误
            return json_response(404, "页码不存在")
    else:
        return json_response(203, "请求方式错误")


# # 获取未审核的文献列表，管理员专属
# @csrf_exempt
# def get_unaudited_files(request):
#     if request.method == 'POST':
#         user = User.objects.filter(email=request.user_info).first()
#         if user.role == 1:
#             files = Document.objects.filter(status=0).values().order_by('-create_time')
#             total = files.count()
#             page = int(request.POST.get('currentpage'))
#             page_size = int(request.POST.get('pageSize'))
#             start = (page - 1) * page_size
#             end = page * page_size
#             files = files[start:end]
#             file_list = []
#             for file in files:
#                 file_dict = {}
#                 file_dict['document_id'] = file['document_id']
#                 file_dict['title'] = file['title']
#                 file_dict['create_time'] = file['create_time']
#                 file_list.append(file_dict)
#             # print(files)
#             data = {'data': file_list, 'total': total}
#             return json_response(200, '请求成功', data)
#         else:
#             return json_response(206, '无权限该操作')
#     else:
#         return json_response(203, '请求方式错误')
#
#
# # 审核文献，管理员专属
# @csrf_exempt
# def examine_file(request):
#     if request.method == 'POST':
#         user = User.objects.filter(email=request.user_info).first()
#         if user.role == 1:
#             data = QueryDict(request.body)
#             file = Document.objects.filter(document_id=data.get('document_id'), status=0).first()
#             if file is None:
#                 return json_response(200, '请求成功', file)
#             file.status = data.get('status')
#             file.reason = data.get('reason')
#             file.auditor = user
#             file.save()
#             file = Document.objects.filter(document_id=data.get('document_id')).values().first()
#             return json_response(200, '请求成功', file)
#         else:
#             return json_response(206, '无权限该操作')
#     else:
#         return json_response(203, '请求方式错误')


# 获取已审核成功的文献列表 管理员专属
# @csrf_exempt
# def get_file_list(request):
#     if request.method == 'GET':
#         user = User.objects.filter(email=request.user_info).first()
#         if user.role == 1:
#             files = Document.objects.select_related('auditor').all().filter(status=1)
#             file_list = []
#             for file in files:
#                 file_dict = {}
#                 file_dict['document_id'] = file.document_id
#                 file_dict['field'] = file.field
#                 file_dict['title'] = file.title
#                 file_dict['create_time'] = file.create_time
#                 file_dict['update_time'] = file.update_time
#                 file_dict['status'] = file.status
#                 file_dict['content'] = file.content
#                 file_dict['author'] = file.auditor.username
#                 file_list.append(file_dict)
#             return json_response(200, '请求成功', file_list)
#         else:
#             return json_response(206, '无权限该操作')
#     else:
#         return json_response(203, '请求方式错误')


# 修改文献，需要对应权限
@csrf_exempt
def change_file(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.user_info).first()
        data = request.POST
        # print(data.get('status'))
        # if int(data.get('status')) != 1:
        #     return json_response(207, '该文献未审核成功')
        if Document.objects.filter(document_id=data.get('document_id')).exists():
            file = Document.objects.filter(document_id=data.get('document_id')).first()
            # file.title = data.get('title')
            file.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.content = data.get('content')
            file.save()
            return json_response(200, '修改成功')
        else:
            return json_response(215, '该文献不存在')
    else:
        return json_response(203, '请求方式错误')


# 删除文献，管理员专属
@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        data = request.POST
        if Document.objects.filter(document_id=data.get('document_id')).exists():
            Document.objects.filter(document_id=data.get('document_id')).delete()
            return json_response(200, '删除成功')
        else:
            return json_response(215, '该文献不存在')
    else:
        return json_response(203, '请求方式错误')

