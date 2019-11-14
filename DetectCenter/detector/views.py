# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from data_processing import *

# ********************************************************************************
#                                                                                *
#                                测试交互接口                               *
#                                                                                *
# ********************************************************************************


class Aaa(APIView):
    """
    测试接口
    """
    def get(self, request, format=None):
        return aaa(request)


    def post(self, request, format=None):
        return aaa(request)

#
class ResetAuditStatus(APIView):
    """
    测试接口
    """
    def get(self, request, format=None):
        return resetAuditState(request)


    def post(self, request, format=None):
        return resetAuditState(request)

# ********************************************************************************
#                                                                                *
#                                与前端检测器交互接口                               *
#                                                                                *
# ********************************************************************************


class Register(APIView):
    """
    注册接口.
    """
    def post(self, request, format=None):
        return register(request)


class ReRegister(APIView):
    """
    重新注册接口.
    """
    def post(self, request, format=None):
        return re_register(request)


class RegisterStatus(APIView):
    """
    注册状态查询接口.
    """
    def get(self, request, format=None):
        return get_register_status(request)


class AuthLogin(APIView):
    """
    认证接口.
    """
    def post(self, request, format=None):
        return auth_login(request)


class BusinessStatusProcess(APIView):
    """
    业务状态处理接口.
    """
    def post(self, request, format=None):
        return process_business_status(request)


class SystemStatusProcess(APIView):
    """
    系统运行状态处理接口.
    """
    def post(self, request, format=None):
        return process_system_status(request)


# ********************************************************************************
#                                                                                *
#                                   与界面交互接口                                 *
#                                                                                *
# ********************************************************************************

class DetectorShow(APIView):
    """
    检测器信息展示
    """
    def get(self, request, format=None):
        return show_all_detectors(request)

    def post(self, request, format=None):
        return show_all_detectors(request)


class DetectorCount(APIView):
    """
    检测器数量
    """
    def get(self, request, format=None):
        return show_detectors_count(request)

    def post(self, request, format=None):
        return show_detectors_count(request)


class DetectorDetail(APIView):
    """
    检测器详情
    """
    def get(self, request, format=None):
        return show_detector_detail(request)

    def post(self, request, format=None):
        return show_detector_detail(request)


class DetectorCheck(APIView):
    """
    检测器审核
    """
    def get(self, request, format=None):
        return check_detector(request)

    def post(self, request, format=None):
        return check_detector(request)


class DetectorEffectivenessUpdate(APIView):
    """
    修改检测器有效性
    """
    def get(self, request, format=None):
        return update_detector_effective_status(request)

    def post(self, request, format=None):
        return update_detector_effective_status(request)

        
class DetectorReportExport(APIView):
    """
    导出检测器统计报表
    """
    def get(self, request, format=None):
        return export_detectors_report(request)

    def post(self, request, format=None):
        return export_detectors_report(request)
        

class DeviceShow(APIView):
    """
    查询设备信息.
    """
    def get(self, request, format=None):
        return show_all_devices(request)

    def post(self, request, format=None):
        return show_all_devices(request)


class DeviceCount(APIView):
    """
    查询设备数量.
    """
    def get(self, request, format=None):
        return show_devices_count(request)

    def post(self, request, format=None):
        return show_devices_count(request)


class DeviceDetail(APIView):
    """
    查询设备详情
    """
    def get(self, request, format=None):
        return show_device_detail(request)

    def post(self, request, format=None):
        return show_device_detail(request)


class DeviceAddUpdate(APIView):
    """
    增加或修改设备信息
    """
    def get(self, request, format=None):
        return add_update_device(request)

    def post(self, request, format=None):
        return add_update_device(request)

class FileUpload(APIView):
    """
    接收文件上传.
    """
    def get(self, request, format=None):
        return common.process_upload_file(request, 'detector_info/')

    def post(self, request, format=None):
        return common.process_upload_file(request, 'detector_info/')

        
class DeviceImport(APIView):
    """
    导入设备信息
    """
    def get(self, request, format=None):
        return import_device_file(request, '')

    def post(self, request, format=None):
        return import_device_file(request, '')
        
        
class TemplateDownload(APIView):
    """
    导入文件模板下载
    """
    def get(self, request, format=None):
        return download_template(request)

    def post(self, request, format=None):
        return download_template(request)


class StatisticDetectorStatus(APIView):
    """
    统计检测器接入状态运行情况
    """
    def get(self, request, format=None):
        return statistics_detector_status(request)

    def post(self, request, format=None):
        return statistics_detector_status(request)


class OnlineEventShow(APIView):
    """
    统计检测器在线事件详情
    """
    def get(self, request, format=None):
        return show_all_devices_online_event(request)

    def post(self, request, format=None):
        return show_all_devices_online_event(request)


class OnlineEventCount(APIView):
    """
    统计检测器在线事件总数
    """
    def get(self, request, format=None):
        return show_devices_online_event_count(request)

    def post(self, request, format=None):
        return show_devices_online_event_count(request)


class DetectorInfoDelete(APIView):
    """
    删除检测器备案信息
    """
    def get(self, request, format=None):
        return detector_info_delete(request)

    def post(self, request, format=None):
        return detector_info_delete(request)


class DetectorDelete(APIView):
    """
    删除检测器备案信息
    """
    def get(self, request, format=None):
        return detector_delete(request)

    def post(self, request, format=None):
        return detector_delete(request)


class AuditModeShow(APIView):
    """
    查询检测器审核模式
    """
    def get(self, request, format=None):
        return detector_audit_mode_show(request)

    def post(self, request, format=None):
        return detector_audit_mode_show(request)


class AuditModeAlert(APIView):
    """
    修改检测器审核模式
    """
    def get(self, request, format=None):
        return detector_audit_mode_alert(request)

    def post(self, request, format=None):
        return detector_audit_mode_alert(request)