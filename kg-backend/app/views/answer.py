from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from app.utils.QuestionMatcher import QuestionMatcher
from app.utils.jsonResponse import json_response
from app.models import User, QApair, Document


# 功能描述：查询相关问答对
# 输入：user_info
# 输出：answer，包含 question
@csrf_exempt
def get_answer(request):
    if request.method == 'POST':
        question = request.POST.get('question')

        qapair = list(QApair.objects.all().values())

        for item in qapair:
            document_id = item.get('document_id')
            document = Document.objects.get(pk=document_id)
            item['title'] = document.title

        matched_question = QuestionMatcher.match_question(question, qapair)

        return json_response(200, '请求成功', matched_question)
    else:
        return json_response(203, '请求方式错误')


# 获取问答对列表，同时需要对每个问答对返回文献名字
# 添加分页功能
@csrf_exempt
def get_answer_list(request):
    if request.method == 'GET':
        answer_list = QApair.objects.all().values()

        # 此处使用 Django 自带的分页查询功能
        # 设置每页显示的记录数，默认一页显示10条记录
        items_per_page = request.GET.get('pageSize', 10)
        paginator = Paginator(answer_list, items_per_page)

        # 获取URL参数中的页码，默认为第一页
        page_number = request.GET.get('page', 1)

        try:
            # 获取指定页码的数据
            current_page = paginator.page(page_number)

            # 将当前页的记录转换成列表
            current_page_data = list(current_page)

            # 在当前页数据中添加 title 字段
            for item in current_page_data:
                document_id = item.get('document_id')
                document = Document.objects.get(pk=document_id)
                item['title'] = document.title

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
            return json_response(200, '请求成功', response_data)
        except EmptyPage:
            # 如果指定的页码不存在，返回404错误
            return json_response(404, "页码不存在")
    else:
        return json_response(203, "请求方式错误")


# 删除问答对
@csrf_exempt
def delete_answer(request):
    if request.method == 'POST':
        # user = User.objects.filter(email=request.user_info).first()
        id = request.POST.get('id')
        # 作为管理员可以删除所有问答对，作为用户可以删除自己的问答对
        # if user.role == 1:
        if QApair.objects.filter(id=id).first() is None:
            return json_response(204, '该问答对不存在')
        else:
            QApair.objects.filter(id=id).first().delete()
        return json_response(200, '删除成功')
    else:
        return json_response(203, '请求方式错误')


# 修改问答对
@csrf_exempt
def change_answer(request):
    if request.method == 'POST':
        data = request.POST
        qapair = QApair.objects.filter(id=data.get('id')).first()
        if qapair is None:
            return json_response(204, '该问答对不存在')
        qapair.question = data.get('question')
        qapair.answer = data.get('answer')
        qapair.save()
        return json_response(200, '修改成功')
    else:
        return json_response(203, '请求方式错误')
