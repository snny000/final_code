# -*- encoding:utf-8 -*-
import json
import traceback
from time import timezone

from django.contrib.auth.models import Permission, Group
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from login.models import User

from DetectCenter import common


def user_query_permission(request):
    """
    用户查询权限
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)

        user_name = request_data.get('username')
        # user_name = "admin"
        user_select = User.objects.filter(username=user_name)
        if user_select.exists():
            result_list = []
            groups = user_select[0].groups.all()
            for group in groups:
                query_result = group.permissions.all()
                for permission in query_result:
                    if len(permission.codename.split('|')) > 1:
                        result_list.append(permission.id)
            # result_list = list(user_select[0].get_all_permissions())
            return common.ui_message_response(200, '查询成功' + json.dumps(result_list), {'permission_id_list': result_list}, status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '用户不存在', '用户不存在')
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                              status.HTTP_500_INTERNAL_SERVER_ERROR)


def group_query_permission(request):
    """
    角色查询权限
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)

        role_id = common.check_request_int_field(request_data, 'role_id')
        if isinstance(role_id, Response):
            return role_id

        result_list = []
        role_select = Group.objects.filter(id=role_id)
        for group in role_select:
            query_result = group.permissions.all()
            for permission in query_result:
                if len(permission.codename.split('|')) > 1:
                    result_list.append(permission.id)
            return common.ui_message_response(200, '查询成功', {'permission_id_list': result_list}, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                              status.HTTP_500_INTERNAL_SERVER_ERROR)


def role_add_permission(request):
    """
    角色增加权限
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)

        role_id = common.check_request_int_field(request_data, 'role_id')
        if isinstance(role_id, Response):
            return role_id
        permission_id_list = common.check_request_list_or_dict_field(request_data, 'permission_id_list')
        if isinstance(permission_id_list, Response):
            return permission_id_list

        role_select = Group.objects.filter(id=role_id)
        if role_select.exists():
            if role_select[0].permissions.all():
                role_select[0].permissions.clear()
            for permission_id in permission_id_list:
                role_select[0].permissions.add(permission_id)
            return common.ui_message_response(200, '角色添加权限成功', 'success', status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '角色不存在', '角色不存在')
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def role_delete_permission(request):
    """
    角色删除权限
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)

        role_id = common.check_request_int_field(request_data, 'role_id')
        if isinstance(role_id, Response):
            return role_id
        permission_id_list = common.check_request_list_or_dict_field(request_data, 'permission_id_list')
        if isinstance(permission_id_list, Response):
            return permission_id_list

        role_select = Group.objects.filter(id=role_id)
        if role_select.exists():
            for permission_id in permission_id_list:
                role_select[0].permissions.remove(permission_id)
            return common.ui_message_response(200, '角色删除权限成功', 'success', status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '角色不存在', '角色不存在')
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def role_delete_all_permission(request):
    """
    角色删除全部权限
    :param request:
    :return:
    """
    try:
        request_data = common.print_header_data(request)

        role_id = common.check_request_int_field(request_data, 'role_id')
        if isinstance(role_id, Response):
            return role_id

        role_select = Group.objects.filter(id=role_id)
        if role_select.exists():
            if role_select[0].permissions.all():
                role_select[0].permissions.clear()
            return common.ui_message_response(200, '角色添加权限成功', 'success', status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '角色不存在', '角色不存在')
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def query_all_permissions(request):
    """
    查询全部权限
    :param request:
    :return:
    """
    try:
        result = {}
        content_type_id_list = []
        result_list = []
        query_result_list = {}
        query_result = Permission.objects.all()
        for permission in query_result:
            content_type_id_list.append(permission.content_type_id)
        content_type_id_list = list(set(content_type_id_list))
        for content_type_id in content_type_id_list:
            query_result = Permission.objects.filter(content_type_id=content_type_id)
            query_result_list_button = []
            for permission in query_result:
                query_result_dict_button = {}
                query_result_dict_menu = {}
                codename_list = permission.codename.split('|')
                if codename_list[-1] == 'menu':
                    query_result_dict_menu['id'] = permission.id
                    query_result_dict_menu['name'] = permission.name
                    query_result_dict_menu['content_type_id'] = permission.content_type_id
                    query_result_list['menu'] = query_result_dict_menu
                elif codename_list[-1] == 'button':
                    query_result_dict_button['id'] = permission.id
                    query_result_dict_button['name'] = permission.name
                    query_result_dict_button['content_type_id'] = permission.content_type_id
                    query_result_list_button.append(query_result_dict_button)
                else:
                    query_result_list_button = []
                    query_result_list = {}
            if query_result_list_button:
                query_result_list['button'] = query_result_list_button
            if query_result_list:
                ss = json.loads(json.dumps(query_result_list))
                result_list.append(ss)
        result['all_permissions'] = result_list
        return common.ui_message_response(200, '查询成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_permission_number(request):
    """
    获取权限数量
    :param request:
    :return:
    """
    try:
        result = {}
        query_result = Permission.objects.all()
        permission_count = query_result.count()
        result['permission_count'] = permission_count
        return common.ui_message_response(200, '查询成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)
