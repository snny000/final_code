# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from rest_framework.parsers import BaseParser, MultiPartParser
from data_processing import *


# ********************************************************************************
#                                                                                *
#                                与前端检测器交互接口                               *
#                                                                                *
# ********************************************************************************

now_date = datetime.datetime.now().strftime('%Y%m%d')
sub_dir = now_date[:6] + '/' + now_date[6:] + '/'  # 文件存储相对路径的子目录


class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()


class CommunicationRelations(APIView):
    """
    通联关系（gzip文件）处理接口.
    """
    parser_classes = (PlainTextParser, MultiPartParser)

    def post(self, request, format=None):
        relative_path = 'communication_relations/' + sub_dir
        return process_communication_relation_upload(request, relative_path)


class ApplicationBehavior(APIView):
    """
    应用行为审计信息(gzip压缩文件)处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'app_behavior/' + sub_dir
        return process_app_behavior_upload(request, relative_path)


class AuditSystem(APIView):
    """
    系统审计信息处理接口.
    """
    def post(self, request, format=None):
        return process_system_audit(request)


# ********************************************************************************
#                                                                                *
#                                   与界面交互接口                                 *
#                                                                                *
# ********************************************************************************


class AuditLogShow(APIView):
    """
    网络行为审计日志信息展示
    """
    def get(self, request, format=None):
        return show_audit_log(request)

    def post(self, request, format=None):
        return show_audit_log(request)


class AuditLogCount(APIView):
    """
    网络行为审计日志信息数量
    """
    def get(self, request, format=None):
        return show_audit_log_count(request)

    def post(self, request, format=None):
        return show_audit_log_count(request)


class SystemAuditShow(APIView):
    """
    系统审计信息展示
    """
    def get(self, request, format=None):
        return show_system_audit(request)

    def post(self, request, format=None):
        return show_system_audit(request)


class SystemAuditCount(APIView):
    """
    系统审计信息数量
    """
    def get(self, request, format=None):
        return show_system_audit_count(request)

    def post(self, request, format=None):
        return show_system_audit_count(request)

        
class LocalAuditShow(APIView):
    """
    管理系统审计信息展示
    """
    def get(self, request, format=None):
        return show_local_audit(request)

    def post(self, request, format=None):
        return show_local_audit(request)
       
       
class LocalAuditCount(APIView):
    """
    管理系统审计信息数量
    """
    def get(self, request, format=None):
        return show_local_audit_count(request)

    def post(self, request, format=None):
        return show_local_audit_count(request)
        
        
class SendLocalAudit(APIView):
    """
    发送管理中心自身审计日志
    """
    def get(self, request, format=None):
        return send_audit(request)

    def post(self, request, format=None):
        return send_audit(request)
        
        
class SendRunningStatus(APIView):
    """
    发送管理中心运行状态
    """
    def get(self, request, format=None):
        return send_running_status(request)

    def post(self, request, format=None):
        return send_running_status(request)

        
class SendCenterInfo(APIView):
    """
    发送管理中心部署信息
    """
    def get(self, request, format=None):
        return send_management_info(request)

    def post(self, request, format=None):
        return send_management_info(request)
        
        
class SendDetectorInfo(APIView):
    """
    发送检测器部署信息
    """
    def get(self, request, format=None):
        return send_detector_info(request)

    def post(self, request, format=None):
        return send_detector_info(request)