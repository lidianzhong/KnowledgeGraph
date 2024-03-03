from django.http import JsonResponse


# 暂时不用
def json_response(code: object = 200, msg: object = '请求成功', data: object = None) -> object:
    """

    :rtype: object
    """
    json_dict = {
        'msg': msg,
    }
    if data is not None:
        json_dict.update({'data': data})
    # 改了一下返回值，加入状态码
    return JsonResponse(json_dict, json_dumps_params={"ensure_ascii": False}, status=code)
