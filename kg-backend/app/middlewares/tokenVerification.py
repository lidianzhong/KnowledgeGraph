from django.utils.deprecation import MiddlewareMixin
from app.utils.jwtAuth import parse_payload
from app.utils.jsonResponse import json_response


# 中间件token验证,验证token是否有效,即是否登录
class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url = request.get_full_path()
        white_list = ['/user/register', '/user/login', '/user/getVerificationCode', '/user/test']
        if url not in white_list:
            token = request.headers.get('Authorization')
            if token:
                result = parse_payload(token)
                if result['data'] is not None:
                    request.user_info = result['data']['email']
                else:
                    return json_response(210, result['error'])
            else:
                return json_response(209, '没有身份信息')
