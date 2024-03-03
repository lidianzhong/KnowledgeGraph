import jwt
import datetime
from jwt import exceptions

SECRET_KEY = "woshishabi"


# 得到token
def create_token(payload, timeout=2000):
    # 声明类型，声明加密算法
    headers = {
        "type": "jwt",
        "alg": "HS256"
    }
    # 设置过期时间
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    result = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256", headers=headers)
    # 返回加密结果
    return result


# 验证token
def parse_payload(token):
    result = {"status": False, "data": None, "error": None}
    try:
        # 进行解密
        verified_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        result["status"] = True
        result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result
