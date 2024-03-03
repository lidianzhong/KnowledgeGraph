from django.views.decorators.csrf import csrf_exempt

from app.models import Log
from app.utils.jsonResponse import json_response
from django.core import serializers


# 获取最新的一项日志
@csrf_exempt
def get_latest_log(request):
    if request.method == 'GET':
        log = Log.objects.all().order_by('-update_time').first()
        return json_response(200, "请求成功", {'log_id': log.log_id,
                                               'update_time': log.update_time,
                                               "log_info": log.log_info,
                                               'vertices_count': log.vertices_count,
                                               'edges_count': log.edges_count,
                                               'qa_count': log.qa_count})
    else:
        return json_response(203, "请求方式错误")


# 获取所有日志
@csrf_exempt
def get_log_list(request):
    if request.method == 'GET':
        logs = Log.objects.all()
        data = []
        for log in logs:
            data.append({'log_id': log.log_id, 'update_time': log.update_time, 'log_info': log.log_info,
                         'vertices_count': log.vertices_count, 'edges_count': log.edges_count, 'qa_count': log.qa_count})
        return json_response(200, "请求成功", data)
    else:
        return json_response(203, "请求方式错误")
