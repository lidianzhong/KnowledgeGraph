from django.db import models
# 将模型映射到数据库中的表

# 用户表
class User(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='user_id')
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.IntegerField(choices=[(0, '普通用户'), (1, '管理员')])
    permission = models.ManyToManyField('Permission', through='UserPermission')

    class Meta:
        db_table = 'user'


# 权限表
class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True, db_column='permission_id', serialize=False)
    permission_name = models.CharField(max_length=50, db_column='permission_name')

    class Meta:
        db_table = 'permission'


# 用户权限表
class UserPermission(models.Model):
    user_permission_id = models.AutoField(primary_key=True, db_column='user_permission_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, db_column='permission_id')
    is_allowed = models.BooleanField(db_column="is_allowed", default=False)

    class Meta:
        db_table = 'user_permission'
        unique_together = ('user_id', 'permission_id')


class Log(models.Model):
    log_id = models.AutoField(primary_key=True, db_column='log_id')
    update_time = models.CharField(max_length=50)
    log_info = models.TextField()  # 模型调用开始/结束（若开始则以下字段可以为空）
    vertices_count = models.IntegerField()  # 新增的点的个数
    edges_count = models.IntegerField()  # 新增的边的个数
    qa_count = models.IntegerField(default=0)  # 新增的边的个数 TODO: fix default value

    class Meta:
        db_table = 'log'


# 文献领域表
# class DocumentField(models.Model):
#     id = models.AutoField(primary_key=True, db_column='id')
#     field_name = models.CharField(max_length=50, db_column='field_name')
#
#     class Meta:
#         db_table = 'document_field'


# 文献表
class Document(models.Model):
    document_id = models.AutoField(primary_key=True, db_column='document_id')
    # field = models.ForeignKey(DocumentField, on_delete=models.CASCADE, db_column='field_id')
    create_time = models.CharField(max_length=50)
    update_time = models.CharField(max_length=50)
    # status = models.IntegerField(choices=[(0, '未审核'), (1, '已审核'), (2, '审核不通过')])
    user_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.TextField()

    # reason = models.CharField(default='', max_length=100)
    # auditor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='auditor')

    class Meta:
        db_table = 'document'


# 问答对表
class QApair(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    # document = models.ForeignKey(Document, on_delete=models.CASCADE, db_column='document_id')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, db_column='document_id')

    class Meta:
        db_table = 'q_a_document'

# class Settings(models.Model):
#     id = models.AutoField(primary_key=True, db_column='id')
#     name = models.CharField(max_length=50, db_column='name')
#     isOpened = models.BooleanField(default=False, db_column='isOpened')
#
#     class Meta:
#         db_table = 'settings'


# class Graph(mongoengine.Document):
#     username = mongoengine.StringField(max_length=32)
#     graph = mongoengine.DictField()
