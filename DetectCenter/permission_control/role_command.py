# -*- encoding:utf-8 -*-
import json
import traceback

from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
# from login.models import *

from DetectCenter import common


def create_role(request):
    """
    创建角色
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        role_name = request_data.get('rolename')
        print role_name
        if role_name is not None:
            query_data = Group.objects.filter(name=role_name)
            if query_data.exists():
                return common.ui_message_response(400, '角色名已经被占用', "角色名已经被占用")
            else:
                group = Group.objects.create(name=role_name)
                group.save()
                return common.ui_message_response(200, '角色创建成功', "success", status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_role(request):
    """
    删除角色
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        role_id_list = common.check_request_list_or_dict_field(request_data, 'role_id_list')
        if isinstance(role_id_list, Response):
            return role_id_list
        for role_id in role_id_list:
            user_query = Group.objects.filter(id=role_id)
            for role in user_query:
                role.delete()
        return common.ui_message_response(200, '角色删除成功', "success", status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def role_to_user(request):
    """
    角色添加用户
    :param request:
    :return:
    """
    result = {}
    result['flag'] = 'failure'
    # role_name = request.get('role_name')
    # user_name = request.get('username')
    role_name = "AverageUser"
    user_name = "yanwang"
    group_select = Group.objects.filter(name=role_name)
    for group in group_select:
        user_select = User.objects.filter(username=user_name)
        for user in user_select:
            group.user_set.add(user)
            result['flag'] = 'success'

    return JsonResponse(result, safe=False)


def role_remove_user(request):
    """
    角色删除用户
    :param request:
    :return:
    """
    result = {}
    result['flag'] = "failure"
    # role_name = request.get('role_name')
    # user_name = request.get('username')
    role_name = "AverageUser"
    user_name = "yanwang"
    group_select = Group.objects.filter(name=role_name)
    for group in group_select:
        user_select = User.objects.filter(username=user_name)
        for user in user_select:
            group.user_set.remove(user)
            result['flag'] = 'success'
    return JsonResponse(result, safe=False)


def role_remove_all_user(request):
    """
    角色删除所有用户
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        role_name = request_data.get('role_name')
        group_select = Group.objects.filter(name=role_name)
        for group in group_select:
            group.user_set.clear()
        return common.ui_message_response(200, '删除成功', '删除成功', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def role_query_all(request):
    """
    查询所有角色的信息
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)
        result = {}
        role_list = []
        role_name = request_data.get('rolename')
        request_data = common.print_header_data(request)
        start_pos, end_pos, page_size = common.get_page_data(request_data)
        if role_name is not None:
            query_terms = {}
            query_terms['name__contains'] = role_name
            query_role = Group.objects.filter(**query_terms)
        else:
            query_role = Group.objects.all()
        query_role = query_role.order_by('-id')
        role_count = query_role.count()
        for role in query_role:
            role_dict = {}
            role_dict['id'] = role.id
            role_dict['name'] = role.name
            role_list.append(role_dict)
        result['query_role'] = role_list[start_pos:end_pos]
        result['role_count'] = role_count

        return common.ui_message_response(200, "查询成功: " + json.dumps(result), result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_role_number(request):
    """
    获取角色数量
    :param request:
    :return:
    """
    try:
        result = {}
        query_result = Group.objects.all()
        role_count = query_result.count()
        result['role_count'] = role_count
        return common.ui_message_response(200, '查询成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)


def change_role_info(request):
    """
    修改角色信息
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)

        role_id = common.check_request_int_field(request_data, 'role_id')
        if isinstance(role_id, Response):
            return role_id

        role_name = request_data.get('rolename')
        if role_name is not None:
            if not Group.objects.filter(id=role_id).exists():
                return common.ui_message_response(400, '该角色不存在', "该角色不存在")
            query_data = Group.objects.filter(name=role_name)
            if query_data.exists():
                return common.ui_message_response(400, '角色名已经被占用', "角色名已经被占用")
            else:
                Group.objects.filter(id=role_id).update(name=role_name)
                return common.ui_message_response(200, '角色信息修改成功', '角色信息修改成功', status.HTTP_200_OK)
        return common.ui_message_response(400, '请求中没有rolename参数', '请求中没有rolename参数')
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '角色信息修改失败', '角色信息修改失败',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)