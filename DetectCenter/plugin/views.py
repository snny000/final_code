# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from data_processing import *
from DetectCenter import file_util as fu


# ********************************************************************************
#                                                                                *
#                                与前端检测器交互接口                               *
#                                                                                *
# ********************************************************************************


class PluginDownload(APIView):
    """
    从服务器下载插件
    """
    def get(self, request, plug_id, format=None):
        return get_plug(request, plug_id)


class PluginPolicyDownload(APIView):
    """
    从服务器获取插件策略
    """
    def get(self, request, plug_id, format=None):
        return get_plug_policy(request, plug_id)


class PluginAlarmFileReport(APIView):
    """
    插件告警上报接口.
    """
    def post(self, request, format=None):
        file_relative_path = 'alarm_plugin/' + fu.get_sub_dir(2)
        return process_plugin_alarm_file(request, file_relative_path)


class PluginStatusReport(APIView):
    """
    插件状态上报接口.
    """
    def post(self, request, format=None):
        return process_plugin_status(request)


# ********************************************************************************
#                                                                                *
#                                   与界面交互接口                                 *
#                                                                                *
# ********************************************************************************


class PluginAlarmShow(APIView):
    """
    查询所有插件告警信息.
    """
    def get(self, request, format=None):
        return show_all_plug_alarm(request)

    def post(self, request, format=None):
        return show_all_plug_alarm(request)


class PluginAlarmCount(APIView):
    """
    查询插件告警数量.
    """
    def get(self, request, format=None):
        return show_plug_alarm_count(request)

    def post(self, request, format=None):
        return show_plug_alarm_count(request)


class PluginStatusShow(APIView):
    """
    查询所有插件状态信息.
    """
    def get(self, request, format=None):
        return show_all_plug_status(request)

    def post(self, request, format=None):
        return show_all_plug_status(request)


class PluginStatusCount(APIView):
    """
    查询插件状态数量.
    """
    def get(self, request, format=None):
        return show_plug_status_count(request)

    def post(self, request, format=None):
        return show_plug_status_count(request)




###############################################################################################
# 测试新添加插件
###############################################################################################

class ShowAllPlug(APIView):
    """
    展示查询插件
    """

    def get(self, request, format=None):
        return show_all_plug(request)

    def post(self, request, format=None):
        return show_all_plug(request)


class ShowPlugCount(APIView):
    """
    统计查询插件数量
    """

    def get(self, request, format=None):
        return show_plug_count(request)

    def post(self, request, format=None):
        return show_plug_count(request)


class AddUpdatePlugin(APIView):
    """
    添加、更新插件，更新插件配置
    """

    def get(self, request, format=None):
        return add_update_plugin(request)

    def post(self, request, format=None):
        return add_update_plugin(request)


class FileUpload(APIView):
    """
    接收插件文件上传.
    """

    def get(self, request, format=None):
        return common.process_upload_file(request, 'plugin/')

    def post(self, request, format=None):
        return common.process_upload_file(request, 'plugin/')


class DeletePlug(APIView):
    """
    删除插件.
    """

    def get(self, request, format=None):
        return delete_plug(request)

    def post(self, request, format=None):
        return delete_plug(request)


class ChangePlug(APIView):
    """
   变更插件生效范围.
    """

    def get(self, request, format=None):
        return change_plug(request)

    def post(self, request, format=None):
        return change_plug(request)

class AppendPlug(APIView):
    """
   追加插件生效范围.
    """

    def get(self, request, format=None):
        return append_plug(request)

    def post(self, request, format=None):
        return append_plug(request)

class PlugSynchronization(APIView):
    """
    插件同步.
    """
    def get(self, request, format=None):
        return plug_synchronization(request)

    def post(self, request, format=None):
        return plug_synchronization(request)

class FulldoseReport2DirectCenter(APIView):
    """
    # 全量同步小类管理中心插件到指挥节点
    """
    def get(self, request, format=None):
        return report_all_plugin_to_direct_center(request)

    def post(self, request, format=None):
        return report_all_plugin_to_direct_center(request)

class JudgePlugGeneration(APIView):
    """
    判断能否生成策略.
    """

    def get(self, request, format=None):
        return judge_plug_generation(request)

    def post(self, request, format=None):
        return judge_plug_generation(request)


class TaskShow(APIView):
    """
    查询所有任务信息.
    """

    def get(self, request, format=None):
        return show_all_tasks(request)

    def post(self, request, format=None):
        return show_all_tasks(request)


class TaskCount(APIView):
    """
    查询任务数量.
    """

    def get(self, request, format=None):
        return show_task_count(request)

    def post(self, request, format=None):
        return show_task_count(request)

class UpdateTaskPlug(APIView):
    """
    将插件任务的状态置为已忽略.
    """

    def get(self, request, format=None):
        return update_task_plug(request)

    def post(self, request, format=None):
        return update_task_plug(request)

class SendAgain(APIView):
    """
    重新下发插件任务.
    """

    def get(self, request, format=None):
        return send_again(request)

    def post(self, request, format=None):
        return send_again(request)


class ProcessDownloadFile(APIView):
    """
    下载插件文件或者下载插件配置文件.
    """

    def get(self, request, save_path, format=None):
        return common.process_download_file(request, 'plugin/', save_path)

    def post(self, request, save_path, format=None):
        return common.process_download_file(request, 'plugin/', save_path)


class StartStopPlug(APIView):
    """
    重新下发插件任务.
    """

    def get(self, request, format=None):
        return start_stop_plugin(request)

    def post(self, request, format=None):
        return start_stop_plugin(request)
