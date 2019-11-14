# -*- encoding:utf-8 -*-
import logging

from rest_framework.views import APIView

from permission_control.permission_command import *
from permission_control.role_command import *
from permission_control.user_command import *

logger = logging.getLogger("django")

class UserRegistration(APIView):
    """
    注册用户信息
    """
    def get(self, request, format=None):
        return user_registration(request)

    def post(self, request, format=None):
        return user_registration(request)


class UserChangePassword(APIView):
    """
    修改密码
    """
    def get(self, request, format=None):
        return user_change_password(request)

    def post(self, request, format=None):
        return user_change_password(request)


class ResetUserPassword(APIView):
    """
    修改密码
    """
    def get(self, request, format=None):
        return reset_user_password(request)

    def post(self, request, format=None):
        return reset_user_password(request)



class UserLogin(APIView):
    """
    用户登录
    """
    def get(self, request, format=None):
        return user_login(request)

    def post(self, request, format=None):
        return user_login(request)


class PasswordExpire(APIView):
    """
    校验密码的有效期
    """
    def get(self, request, format=None):
        return is_pwd_expire(request)

    def post(self, request, format=None):
        return is_pwd_expire(request)


class UserQueryAll(APIView):
    """
    查询所有用户信息
    """
    def get(self, request, format=None):
        return user_query_all(request)

    def post(self, request, format=None):
        return user_query_all(request)


class UserLogout(APIView):
    """
    用户注销
    """
    def get(self, request, format=None):
        return user_logout(request)

    def post(self, request, format=None):
        return user_logout(request)


class CreateRole(APIView):
    """
    创建角色
    """
    def get(self, request, format=None):
        return create_role(request)

    def post(self, request, format=None):
        return create_role(request)


class DeleteRole(APIView):
    """
    删除角色
    """
    def get(self, request, format=None):
        return delete_role(request)

    def post(self, request, format=None):
        return delete_role(request)


class UserToRole(APIView):
    """
    用户选择角色
    """
    def get(self, request, format=None):
        return user_to_role(request)

    def post(self, request, format=None):
        return user_to_role(request)


class RoleToUser(APIView):
    """
    角色选择用户
    """
    def get(self, request, format=None):
        return role_to_user(request)

    def post(self, request, format=None):
        return role_to_user(request)


class UserRemoveRole(APIView):
    """
    用户退出角色选择
    """
    def get(self, request, format=None):
        return user_remove_role(request)

    def post(self, request, format=None):
        return user_remove_role(request)


class UserRemoveAll(APIView):
    """
    用户退出所有角色
    :return:
    """
    def get(self, request, format=None):
        return user_remove_all(request)

    def post(self, request, format=None):
        return user_remove_all(request)


class RoleRemoveUser(APIView):
    """
    角色删除用户
    :return:
    """
    def get(self, request, format=None):
        return role_remove_user(request)

    def post(self, request, format=None):
        return role_remove_user(request)


class RoleRemoveAllUser(APIView):
    """
    角色删除所有用户
    :param request:
    :return:
    """
    def get(self, request, format=None):
        return role_remove_all_user(request)

    def post(self, request, format=None):
        return role_remove_all_user(request)


class UserQueryPermission(APIView):
    """
    查询用户的权限
    :param APIView:
    :return:
    """
    def get(self, request, format=None):
        return user_query_permission(request)

    def post(self, request, format=None):
        return user_query_permission(request)


class DeleteUser(APIView):
    """
    删除用户信息
    """
    def get(self, request, format=None):
        return delete_user(request)

    def post(self, request, format=None):
        return delete_user(request)


class ChangeUserInfo(APIView):
    """
    修改用户信息
    """
    def get(self, request, format=None):
        return change_user_info(request)

    def post(self, request, format=None):
        return change_user_info(request)


class RoleQueryPermission(APIView):
    """
    角色查询权限
    :param APIView:
    :return:
    """
    def get(self, request, format=None):
        return group_query_permission(request)

    def post(self, request, format=None):
        return group_query_permission(request)


class RoleAddPermission(APIView):
    """
    角色增加权限
    :param APIView:
    :return:
    """
    def get(self, request, format=None):
        return role_add_permission(request)

    def post(self, request, format=None):
        return role_add_permission(request)


class RoleDeletePermission(APIView):
    """
    角色删除权限
    :param APIView:
    :return:
    """
    def get(self, request, format=None):
        return role_delete_permission(request)

    def post(self, request, format=None):
        return role_delete_permission(request)


class RoleDeleteAllPermission(APIView):
    """
    角色删除所有权限
    :param APIView:
    :return:
    """
    def get(self, request, format=None):
        return role_delete_all_permission(request)

    def post(self, request, format=None):
        return role_delete_all_permission(request)


class QueryAllPermissions(APIView):
    """
    查询所有权限
    """
    def get(self, request, format=None):
        return query_all_permissions(request)

    def post(self, request, format=None):
        return query_all_permissions(request)


class RoleQueryAll(APIView):
    """
    查询所有角色信息
    """
    def get(self, request, format=None):
        return role_query_all(request)

    def post(self, request, format=None):
        return role_query_all(request)

class GetRoleNumber(APIView):
    """
    获取角色数量
    """
    def get(self, request, format=None):
        return get_role_number(request)

    def post(self, request, format=None):
        return get_role_number(request)


class GetUserNumber(APIView):
    """
    获取用户数量
    """
    def get(self, request, format=None):
        return get_user_number(request)

    def post(self, request, format=None):
        return get_user_number(request)

class GetPermissionNumber(APIView):
    """
    获取用户数量
    """
    def get(self, request, format=None):
        return get_permission_number(request)

    def post(self, request, format=None):
        return get_permission_number(request)


class ChangeRoleInfo(APIView):
    """
    修改角色信息
    """
    def get(self, request, format=None):
        return change_role_info(request)

    def post(self, request, format=None):
        return change_role_info(request)


if __name__ == '__main__':
    # add_detect()
    pass