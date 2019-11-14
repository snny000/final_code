# -*- encoding:utf-8 -*-
import traceback


from django.contrib.auth.models import Group

from django.contrib import auth
from login.models import User
from rest_framework import status
from rest_framework.response import Response

from DetectCenter import common, date_util as du, security_util as su
from login import login_common as lc

USERNAME = ''

import sys

reload(sys)
sys.setdefaultencoding('utf-8')



# @_auth('login.add_user')
def user_registration(request):
    """
    注册用户信息，创建用户名和密码,auth模块不存储用户密码明文而是存储一个Hash值, 比如迭代使用Md5算法.
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        user_data = lc.trans_user_registration_info(request_data)
        if 'password' not in user_data:
            user_data['password'] = str(su.get_md5('123456')).upper()
        user_name = user_data['username']
        if 'role_id' in user_data:
            role_id = user_data['role_id']
            del user_data['role_id']
        else:
            role_id = 3  # 默认角色
        user_data['is_active'] = '1'
        user_data['is_staff'] = '1'
        print "user_data:", user_data
        if user_data:
            query_data = User.objects.filter(username=user_name)
            if query_data.exists():
                common.generate_system_log(request_data, u'用户操作', u'注册操作', user_name + u'注册失败，用户名被占用')
                return common.ui_message_response(400, '用户名已经被占用', "用户名已经被占用")
            else:
                user = User.objects.create_user(**user_data)
                user.save()
                if role_id:
                    group_select = Group.objects.filter(id=role_id)
                    for group in group_select:
                        user.groups.add(group)
                common.generate_system_log(request_data, u'用户操作', u'注册操作', user_name + u'注册成功')
                return common.ui_message_response(200, '用户注册成功', "success", status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        common.generate_system_log(request_data, u' 用户操作', u'注册操作', user_name + u'注册失败，注册出现错误')
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# def user_authenticate(request):
#     """
#     authenticate模块校验用户,认证用户的密码是否有效, 若有效则返回代表该用户的user对象, 若无效则返回None。需要注意的是：该方法不检查is_active标志位。
#     :param request:
#     :return:
#     """
#     result = {}
#     user_data = trans_user_authenticate_info(request)
#     user = authenticate(**user_data)
#     if user:
#         print user
#         result['flag'] = "success"
#     else:
#         result['flag'] = "failure"
#     return JsonResponse(result, safe=False)


def user_change_password(request):
    """
    修改用户密码
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        user_data = lc.trans_user_change_password(request_data)
        print user_data
        username = user_data['username']
        user = auth.authenticate(**{'username': username, 'password': user_data['old_password']})
        if user is not None:
            user.set_password(user_data['new_password'])
            user.save()
            User.objects.filter(username=username).update(last_update_time=du.get_current_time())
            common.generate_system_log(request_data, u' 用户操作', u'修改密码操作', username + u'修改密码成功')
            return common.ui_message_response(200, '修改密码成功', "success", status.HTTP_200_OK)
        else:
            common.generate_system_log(request_data, u' 用户操作', u'修改密码操作', username + u'修改密码失败')
            return common.ui_message_response(400, '原密码输入错误', '原密码输入错误')
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def reset_user_password(request):
    """
    重置用户密码
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        user_data = lc.trans_user_change_password(request_data)
        user = User.objects.get(id=user_data['id'])
        username = user.username
        if user is not None:
            user.set_password(str(su.get_md5('123456')).upper())
            user.save()
            User.objects.filter(username=username).update(last_update_time=du.get_current_time())
            common.generate_system_log(request_data, u' 用户操作', u'重置密码操作', username + u'重置密码成功')
            return common.ui_message_response(200, '修改密码成功', "success", status.HTTP_200_OK)
        else:
            common.generate_system_log(request_data, u' 用户操作', u'重置密码操作', username + u'重置密码失败')
            return common.ui_message_response(400, '用户不存在', '用户不存在')
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_login(request):
    """
    登录校验
    :param request:
    :return:
    """
    try:
        result = {}
        user_data = {}
        role_result = {}
        request_data = common.print_header_data(request)
        username = request_data.get('username')
        # user_data['username'] = 'admin'
        # username = 'admin'
        user_data['username'] = username
        password = request_data.get('password')
        # user_data['password'] = str(su.get_md5('123456')).upper()
        # password = str(su.get_md5('123456')).upper()
        user_data['password'] = password
        if User.objects.filter(username=username):
            user = auth.authenticate(**user_data)
            if user:
                # django.contrib.auth.login(request, user)
                result['username'] = user_data['username']
                user_query = User.objects.filter(username=result['username'])
                user_query.update(last_login=du.get_current_time())
                group_query = user_query[0].groups.all()
                for group in group_query:
                    permission_id_list = []
                    permission_query = group.permissions.all()
                    for permission in permission_query:
                        permission_id_list.append(permission.id)
                    role_result[group.name] = permission_id_list

                result['role'] = role_result
                common.generate_system_log(request_data, u'用户操作', u'登录操作', username + u'登录成功')
                result['flag'] = "success"
                print "login result:", result
                return common.ui_message_response(200, '登录成功', result, status.HTTP_200_OK)
            else:
                common.generate_system_log(request_data, u'用户操作', u'登录操作', username + u'密码错误')
                return common.ui_message_response(400, '密码错误', '密码错误')
        else:
            common.generate_system_log(request_data, u'用户操作', u'登录操作', u'用户名不存在')
            return common.ui_message_response(400, '用户名不存在', '用户名不存在')
    except Exception:
        traceback.print_exc()
        common.generate_system_log(request_data, u'用户操作', u'登录操作', u'登录模块出现异常')
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 判断密码是否过期
def is_pwd_expire(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        login_id = request_data.get('username')  # 用户id
        if login_id is not None:
            query_data = User.objects.filter(username=login_id)
            now_time = du.get_current_time()
            if now_time - query_data[0].last_update_time >= common.EXPIRE_TIME:
                # is_expire = 1
                is_expire = 0
            else:
                is_expire = 0
            return common.ui_message_response(200, '过期' if is_expire == 1 else '未过期', is_expire, status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '没有username参数', "参数为空")
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                              status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    # logout(request)
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        login_id = request_data.get('username')
        if login_id is not None:
            common.generate_system_log(request_data, u'用户操作', u'注销操作', login_id + u'注销成功')
            return common.ui_message_response(200, '注销成功', '注销成功', status.HTTP_200_OK)
        else:
            common.generate_system_log(request_data, u'用户操作', u'注销操作', u'用户名未知')
            return common.ui_message_response(400, '用户名参数为空', "用户名参数为空")

    except Exception:
        common.generate_system_log(request_data, u'用户操作', u'注销操作', u'注销模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 校验权限的装饰器
def permission_required(username, permission):
    user = User.objects.get(username=username)

    def decorator(f):
        def decorated_function(*args, **kwargs):
            if user.has_perm(permission):
                newf = f(*args, **kwargs)
                return newf

        return decorated_function

    return decorator


# from django.contrib.auth.decorators import permission_required, login_required


# @login_required(login_url='/login/user_login/')
# @permission_required(USERNAME, 'auth.add_user')
def user_query_all(request):
    """
    检索账户信息
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        result = {}
        user_list = []
        query_terms = {}
        role_id = ''
        if 'role_id' in request_data:
            role_id = request_data.get('role_id')
        if 'username' in request_data:
            username = request_data.get('username')
            query_terms['username__contains'] = username
        start_pos, end_pos, page_size = common.get_page_data(request_data)
        if query_terms:
            query_result = User.objects.filter(**query_terms)
        else:
            query_result = User.objects.all()
        if role_id:
            user_result_list = []
            query_result = query_result.order_by('-id')
            for user in query_result:
                role_query = user.groups.all()
                for role in role_query:
                    if role.id == int(role_id):
                        user_result_list.append(user)
            for user in user_result_list:
                user_dict = {}
                user_dict['id'] = user.id
                user_dict['username'] = user.username
                role_query = user.groups.all()
                if len(role_query) > 0:
                    role_name_list = []
                    role_id_list = []
                    for role in role_query:
                        role_name_list.append(role.name)
                        role_id_list.append(role.id)
                    user_dict['role_name'] = role_name_list
                    user_dict['role_id'] = role_id_list
                user_list.append(user_dict)
        else:
            user_count = query_result.count()
            query_result = query_result.order_by('-id')
            for user in query_result:
                user_dict = {}
                user_dict['id'] = user.id
                user_dict['username'] = user.username
                role_query = user.groups.all()
                if len(role_query) > 0:
                    role_name_list = []
                    role_id_list = []
                    for role in role_query:
                        role_name_list.append(role.name)
                        role_id_list.append(role.id)
                    user_dict['role_name'] = role_name_list
                    user_dict['role_id'] = role_id_list
                user_list.append(user_dict)
        print user_list
        result['user_query'] = user_list[start_pos:end_pos]
        result['user_count'] = len(user_list)

        print "query_user:", result
        #return JsonResponse(result, safe=False)
        return common.ui_message_response(200, '查询用户成功', result, status_code=status.HTTP_200_OK)

    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_user_number(request):
    """
    获取用户数量
    :param request:
    :return:
    """
    try:
        result = {}
        query_terms = {}
        request_data = common.print_header_data(request)
        query_result = User.objects.filter(**query_terms)
        user_count = query_result.count()
        result['user_count'] = user_count
        return common.ui_message_response(200, '查询成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_to_role(request):
    """
    用户选择角色
    :param request:
    :return:
    """
    try:
        # username = request.get('username')
        # role_name = request.get('rolename')
        username = "sunwukong"
        role_name = "系统管理员"
        user_select = User.objects.filter(username=username)
        for user in user_select:
            group_select = Group.objects.filter(name=role_name)
            for group in group_select:
                user.groups.add(group)
        return common.ui_message_response(200, '给用户' + username + "设置角色" + role_name + "成功", 'success', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_remove_role(request):
    """
    用户退出角色选择
    :param request:
    :return:
    """
    try:
        # username = request.get('username')
        # role_name = request.get('rolename')
        username = "wangyan"
        role_name = "AverageUser"
        user_select = User.objects.filter(username=username)
        for user in user_select:
            group_select = Group.objects.filter(name=role_name)
            for group in group_select:
                user.groups.remove(group)
        return common.ui_message_response(200, '给用户' + username + "删除角色" + role_name + "成功", 'success', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_remove_all(request):
    """
    用户退出所有角色
    :param request:
    :return:
    """
    try:
        # username = request.get('username')
        username = "sunwukong"
        user_select = User.objects.filter(username=username)
        for user in user_select:
            user.groups.clear()
        return common.ui_message_response(200, '给用户' + username + "清空角色成功", 'success',
                                              status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_user(request):
    """
    根据用户id删除用户信息
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        user_id_list = common.check_request_list_or_dict_field(request_data, 'user_id_list')
        if isinstance(user_id_list, Response):
            return user_id_list

        for user_id in user_id_list:
            user_query = User.objects.filter(id=user_id)
            for user in user_query:
                user.groups.clear()
                user.delete()
        return common.ui_message_response(200, '用户删除成功', 'success', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '用户删除失败', '用户删除失败',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def change_user_info(request):
    """
    修改用户信息
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        user_id = common.check_request_int_field(request_data, 'user_id')
        if isinstance(request_data, Response):
            return user_id
        username = request_data.get('username')
        role_id = common.check_request_list_or_dict_field(request_data, 'role_id')
        if isinstance(role_id, Response):
            return role_id
        if username:
            User.objects.filter(id=user_id).update(username=username)
        user_query = User.objects.filter(id=user_id)
        if user_query.exists():
            if user_query[0].groups.all():
                user_query[0].groups.clear()
            group_select = Group.objects.filter(id__in=role_id)
            for group in group_select:
                user_query[0].groups.add(group)
        else:
            return common.ui_message_response(400, '用户不存在', '用户不存在')
        return common.ui_message_response(200, '用户信息修改成功', '用户信息修改成功', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)

