from django.urls import path
from app.views import user, file, permission, graph, answer, log

urlpatterns = [

    path(r'user/register', user.register),
    path(r'user/login', user.login),
    # path(r'user/logoff', user.logoff), 前端实现
    path(r'user/getUserList', user.get_user_list),
    path(r'user/deleteSelf', user.delete_self),
    path(r'user/getVerificationCode', user.verification_code),
    path(r'user/test', user.test),

    path(r'file/uploadFile', file.upload_file), # 上传文献
    path(r'file/getAllFiles', file.get_all_files), # 查询所有文献（分页）
    path(r'file/getFileDetail', file.get_file_detail), # 查询单个文献
    path(r'file/changeFile', file.change_file),
    path(r'file/deleteFile', file.delete_file),

    path(r'permission/getUserPermission', permission.get_user_permission),
    path(r'permission/changePermission', permission.change_permission),
    path(r'permission/grantAdmin', permission.grant_admin),
    path(r'permission/deleteUser', permission.delete_user),

    path(r'graph/getGraph', graph.get_graph),

    path(r'answer/getSimilarAnswer', answer.get_answer),
    path(r'answer/getAnswerList', answer.get_answer_list),
    path(r'answer/deleteAnswer', answer.delete_answer),
    path(r'answer/changeAnswer', answer.change_answer),

    path(r'log/getLatestLog', log.get_latest_log),
    path(r'log/getLogList', log.get_log_list),
]
