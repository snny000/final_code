# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from data_processing import *

import policy_common as pc



# ********************************************************************************
#                                                                                *
#                                   与界面交互接口                                 *
#                                                                                *
# ********************************************************************************


# rule group views
class UpdateGroup(APIView):
    """
    更新某个监测模块的规则的所属任务组.
    """
    def get(self, request, format=None):
        return rule_update_group(request)

    def post(self, request, format=None):
        return rule_update_group(request)


class CopyRuleGroup(APIView):
    """
    复制某个监测模块的规则的信息.
    """
    def get(self, request, format=None):
        return copy_policy(request)

    def post(self, request, format=None):
        return copy_policy(request)



class RuleShow(APIView):
    """
    查询某个监测模块的所有规则信息.
    """
    def get(self, request, format=None):
        return show_all_rules(request)

    def post(self, request, format=None):
        return show_all_rules(request)


class RuleCount(APIView):
    """
    查询某个监测模块的规则数量.
    """
    def get(self, request, format=None):
        return show_rules_count(request)

    def post(self, request, format=None):
        return show_rules_count(request)


class RuleCountAll(APIView):
    """
    查询所有监测模块的规则数量.
    """
    def get(self, request, format=None):
        return show_rules_count_all(request)

    def post(self, request, format=None):
        return show_rules_count_all(request)


class RuleInsert(APIView):
    """
    插入某个监测模块的规则.
    """
    def get(self, request, format=None):
        return insert_rule(request)

    def post(self, request, format=None):
        return insert_rule(request)


class FileUpload(APIView):
    """
    接收文件上传.
    """
    def get(self, request, format=None):
        return common.process_upload_file(request, 'policy/')

    def post(self, request, format=None):
        return common.process_upload_file(request, 'policy/')

      
class RuleTemplateDownload(APIView):
    """
    导入规则文件模板下载
    """
    def get(self, request, format=None):
        return download_rule_template(request)

    def post(self, request, format=None):
        return download_rule_template(request)
        

class RuleBatchInsert(APIView):
    """
    批量插入某个监测模块的规则.
    """
    def get(self, request, format=None):
        return batch_insert_rules(request, '')

    def post(self, request, format=None):
        return batch_insert_rules(request, '')


class RuleDelete(APIView):
    """
    删除某个监测模块的规则.
    """
    def get(self, request, format=None):
        return delete_rules(request)

    def post(self, request, format=None):
        return delete_rules(request)


class RuleDetectorChange(APIView):
    """
    变更策略生效的检测器范围
    """
    def get(self, request, format=None):
        return change_rules_detectors(request)

    def post(self, request, format=None):
        return change_rules_detectors(request)


class RuleDetectorAppend(APIView):
    """
    追加策略生效的检测器范围
    """
    def get(self, request, format=None):
        return append_rules_detector(request)

    def post(self, request, format=None):
        return append_rules_detector(request)


class LabelModify(APIView):
    """
    批量修改规则标签
    """
    def get(self, request, format=None):
        return modify_labels(request)

    def post(self, request, format=None):
        return modify_labels(request)


class PolicyGenerate(APIView):
    """
    生成某个监测模块的策略.
    """
    def get(self, request, format=None):
        operate_type = common.check_request_int_field(request.GET, 'type')   # 操作类型（0：增量，1：全量）
        if isinstance(operate_type, Response):
            return operate_type
        if operate_type == 0:
            return generate_increment_policy(request)
        else:
            return generate_fulldose_policy(request)

    def post(self, request, format=None):
        operate_type = common.check_request_int_field(request.data, 'type')  # 操作类型（0：增量，1：全量）
        if isinstance(operate_type, Response):
            return operate_type
        if operate_type == 0:
            return generate_increment_policy(request)
        else:
            return generate_fulldose_policy(request)


class FulldoseReport2DirectCenter(APIView):
    """
    # 全量同步小类管理中心插件到指挥节点
    """
    def get(self, request, format=None):
        return report_all_rule_to_direct_center(request)

    def post(self, request, format=None):
        return report_all_rule_to_direct_center(request)


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


class IgnorePolicyTask(APIView):
    """
    将策略任务的状态置为已忽略.
    """

    def get(self, request, format=None):
        return update_to_unvalid(request, True, u'策略任务')

    def post(self, request, format=None):
        return update_to_unvalid(request, True, u'策略任务')


class PolicyTaskSendAgain(APIView):
    """
    重新下发策略任务.
    """
    def get(self, request, format=None):
        return send_again(request, True, u'策略操作')

    def post(self, request, format=None):
        return send_again(request, True, u'策略操作')


class CommandGenerate(APIView):
    """
    生成命令.
    """
    def get(self, request, format=None):
        return generate_command(request)

    def post(self, request, format=None):
        return generate_command(request)


class CommandFileUpload(APIView):
    """
    接收命令上传文件
    """

    def get(self, request, format=None):
        return common.process_upload_file(request, 'command/')

    def post(self, request, format=None):
        return common.process_upload_file(request, 'command/')


class CommandShow(APIView):
    """
    查询所有命令信息.
    """
    def get(self, request, format=None):
        return show_all_commands(request)

    def post(self, request, format=None):
        return show_all_commands(request)


class CommandCount(APIView):
    """
    查询命令数量.
    """
    def get(self, request, format=None):
        return show_command_count(request)

    def post(self, request, format=None):
        return show_command_count(request)


class IgnoreCommandTask(APIView):
    """
    将策略任务的状态置为已忽略.
    """

    def get(self, request, format=None):
        return update_to_unvalid(request, False, u'命令任务')

    def post(self, request, format=None):
        return update_to_unvalid(request, False, u'命令任务')


class CommandTaskSendAgain(APIView):
    """
    重新下发策略任务.
    """
    def get(self, request, format=None):
        return send_again(request, False, u'命令操作')

    def post(self, request, format=None):
        return send_again(request, False, u'命令操作')


class JudgePolicyGeneration(APIView):
    """
    判断能否生成策略.
    """
    def get(self, request, format=None):
        return judge_policy_generation(request)

    def post(self, request, format=None):
        return judge_policy_generation(request)


# ********************************************************************************
#                                                                                *
#                                与前端检测器交互接口                               *
#                                                                                *
# ********************************************************************************


class HeartbeatProcess(APIView):
    """
    心跳信息处理接口.
    """
    def post(self, request, format=None):
        return process_heartbeat(request)


class TimeSync(APIView):
    """
    时间同步处理接口.
    """
    def get(self, request, format=None):
        return sync_time(request)


class FirmwareUpdate(APIView):
    """
    固件升级文件下载处理接口
    """
    def get(self, request, format=None):
        return download_update_firmware(request, '')

    def post(self, request, format=None):
        return download_update_firmware(request, '')


class VersionCheck(APIView):
    """
    版本一致性检查上报处理接口
    """
    def post(self, request, format=None):
        return process_version_check(request)


class InnerPolicy(APIView):
    """
    内置策略更新文件下载处理接口
    """
    def get(self, request, format=None):
        return download_inner_policy(request, '')

    def post(self, request, format=None):
        return download_inner_policy(request, '')
