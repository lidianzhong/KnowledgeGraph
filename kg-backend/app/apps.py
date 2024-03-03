from django.apps import AppConfig
from django.db.models.signals import post_migrate
import hashlib


# 初始化数据库
def init_account(sender, **kwargs):
    from app.models import User, Permission
    if not User.objects.filter(username='admin').exists():
        password = "1234"
        encry = hashlib.md5()
        encry.update(password.encode())
        md5_pwd = encry.hexdigest()  # 密码加密
        # 创建超级管理员
        User.objects.create(username='admin', password=md5_pwd, email="admin@qq.com", role=1)
        # 创建权限
        Permission.objects.create(permission_name="changeFile")
        Permission.objects.create(permission_name="deleteFile")
        Permission.objects.create(permission_name="changeAnswer")
        Permission.objects.create(permission_name="deleteAnswer")


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        post_migrate.connect(init_account, sender=self)
