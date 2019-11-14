# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from data_processing import *
import detect_center_reg_auth


# ********************************************************************************
#                                                                                *
#                             与指挥中心交互接口                                 *
#                                                                                *
# ********************************************************************************


class PolicyReception(APIView):
    """
    接收指挥中心的策略
    """
    def get(self, request, format=None):
        return receive_policy(request)

    def post(self, request, format=None):
        return receive_policy(request)
        
        
class PlugReception(APIView):
    """
    接收指挥中心的插件
    """
    def get(self, request, format=None):
        return receive_plug(request)

    def post(self, request, format=None):
        return receive_plug(request)


# class PlugReceptionFile(APIView):
#     """
#     接收指挥中心的插件
#     """
#     def get(self, request, format=None):
#         return receive_plug_file(request)
#
#     def post(self, request, format=None):
#         return receive_plug_file(request)


class CmdReceptionFile(APIView):
    """
    接收指挥中心的插件
    """
    def get(self, request, format=None):
        return receive_cmd(request)

    def post(self, request, format=None):
        return receive_cmd(request)

        
class AuditResult(APIView):
    """
    接收指挥中心返回审核结果
    """
    def post(self, request, format=None):
        return obtain_register_status(request)


# ********************************************************************************
#                                                                                *
#                             与管理中心UI交互接口                                 *
#                                                                                *
# ********************************************************************************
class CenterShow(APIView):
    """
    查询管理中心信息
    """
    def get(self, request, format=None):
        return center_show(request)

    def post(self, request, format=None):
        return center_show(request)


class CenterRegister(APIView):
    """
    注册管理中心
    """
    def get(self, request, format=None):
        return center_register(request)

    def post(self, request, format=None):
        return center_register(request)


class CenterAuth(APIView):
    """
    认证管理中心
    """
    def get(self, request, format=None):
        return center_auth(request)

    def post(self, request, format=None):
        return center_auth(request)


class CenterReset(APIView):
    """
    重置管理中心
    """
    def get(self, request, format=None):
        return center_reset(request)

    def post(self, request, format=None):
        return center_reset(request)


class CenterUpdateIpWhitelist(APIView):
    """
    修改管理中心IP白名单
    """
    def get(self, request, format=None):
        return center_update_ip_whitelist(request)

    def post(self, request, format=None):
        return center_update_ip_whitelist(request)


class CenterSaveDirectorConfig(APIView):
    """
    配置指挥节点数据
    """
    def get(self, request, format=None):
        return center_save_director_config(request)

    def post(self, request, format=None):
        return center_save_director_config(request)


class DownloadPlug(APIView):
    """
    重新下发插件任务.
    """

    def get(self, request, format=None):
        return download_plug(request)

    def post(self, request, format=None):
        return download_plug(request)