# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from task_group_processing import *

import policy_common as pc



# ********************************************************************************
#                                                                                *
#                                   与界面交互接口                                 *
#                                                                                *
# ********************************************************************************


class TaskGroupProcess(APIView):
    """
    任务组操作
    """
    def get(self, request, format=None):
        return task_group_show(request)

    def post(self, request, format=None):
        return task_group_show(request)


class GetTaskPolicy(APIView):
    """
    任务组查询策略操作
    """
    def get(self, request, format=None):
        return group_rule_show(request)

    def post(self, request, format=None):
        return group_rule_show(request)

class AddOrUpdateTaskgroup(APIView):
    """
    添加或修改任务组
    """
    def get(self, request, format=None):
        return add_update_taskgroup(request)

    def post(self, request, format=None):
        return add_update_taskgroup(request)

class DeleteTaskGroup(APIView):
    """
    批量删除任务组
    """
    def get(self, request, format=None):
        return delete_taskgroup(request)

    def post(self, request, format=None):
        return delete_taskgroup(request)

class UpdateBatchTaskgroup(APIView):
    """
    批量修改任务组
    """
    def get(self, request, format=None):
        return update_batch_taskgroup(request)

    def post(self, request, format=None):
        return update_batch_taskgroup(request)


class GetTaskPolicyCount(APIView):
    """
    获取某一任务策略总数
    """
    def get(self, request, format=None):
        return group_rule_count(request)

    def post(self, request, format=None):
        return group_rule_count(request)


class GetTaskCount(APIView):
    """
    获取某一查询条件下任务总数
    """

    def get(self, request, format=None):
        return task_group_count(request)

    def post(self, request, format=None):
        return task_group_count(request)