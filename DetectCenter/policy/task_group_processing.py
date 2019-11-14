# -*- encoding:utf-8 -*-
import json
import traceback
import time
import datetime
from django.core.serializers import serialize
from django.db import connection

from rest_framework import status
from rest_framework.response import Response

from DetectCenter import common, date_util as du
from policy.data_processing import rule_models
from policy.models import TaskGroup
from policy.policy_serializers import TaskGroupSerializer


# 构建任务组查询条件,返回查询数据
def get_group_query_terms(request_data):
    query_terms = {}
    group_id = request_data.get('group_id')
    name = request_data.get('name')
    rule_type = request_data.get('rule_type')
    create_person = request_data.get('create_person')
    time_min = request_data.get('time_min')  # 任务生成起始时间
    time_max = request_data.get('time_max')
    if group_id is not None:
        query_terms['group_id__contains'] = group_id  # 任务id模糊查询
    if name is not None:
        query_terms['name__contains'] = name
    if rule_type is not None:
        query_terms['rule_type'] = rule_type
    if create_person is not None:
        query_terms['create_person__contains'] = create_person
    if time_min is not None:  # 产生时间筛选
        query_terms['create_time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    if time_max is not None:
        query_terms['create_time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)
    query_data = TaskGroup.objects.filter(**query_terms)
    return query_data


# 查询任务组信息
def task_group_show(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_data = get_group_query_terms(request_data)  # 获取查询后的数据
        query_data = query_data.order_by('-id')[start_pos:end_pos]
        serializer_data = serialize('json', query_data,
                                    fields=('group_id', 'name', 'rule_type', 'create_person', 'create_time', 'rule_id_list',
                                        'remarks'))
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']

            fields['group_id'] = str(fields['group_id'])
            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


#  在某一查询条件下，任务组总数
def task_group_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_data = get_group_query_terms(request_data)  # 获取查询结果

        count = query_data.count()  # 查询数量（与查询接口对应）
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 构造简单策略查询条件：通过任务组task_id去查询某一任务组所有策略
def get_group_rule_query(request_data):
    policy_type = common.check_request_int_field(request_data, 'policy_type')
    if isinstance(policy_type, Response):
        return policy_type

    # 构造查询参数
    query_terms = {}

    # 通用查询参数
    group_id = common.check_request_int_field(request_data, 'group_id')  # 任务组ID
    if isinstance(group_id, Response):
        return group_id

    query_terms['group_id'] = group_id  # 查询
    query_data = rule_models[policy_type - 1].objects.filter(**query_terms).filter(is_del=1)
    return query_data


# 查询任务组对应的策略信息
def group_rule_show(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_data = get_group_rule_query(request_data)  # 获取查询条件
        if isinstance(query_data, Response):
            return query_data

        query_data = query_data.order_by('-id')[start_pos:end_pos]
        serializer_data = serialize('json', query_data)
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']
            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询某个策略模块的规则总数
def group_rule_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_data = get_group_rule_query(request_data)  # 获取查询结果

        count = query_data.count()  # 查询数量（与查询接口对应）
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 添加任务组
def add_update_taskgroup(request):
    try:
        # print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        request_data = common.print_header_data(request)  # 获取请求数据
        data = common.check_request_list_or_dict_field(request_data, 'json')
        if isinstance(data, Response):
            return data

        with connection.cursor() as cursor:  # 运行mysql函数，生成规则id
            cursor.execute('select nextval(%s)', ('task_group',))  # 参数是一个元组
            group_id = common.get_rule_serial(cursor.fetchone()[0])

        operate_data = {
            'group_id': group_id,
            'name': data['name'],
            'rule_type': data['rule_type'],
            'create_person': data['create_person'],
            'create_time': du.get_current_date_string(),
            'remarks': data['remarks']
        }

        print "##########", operate_data
        if data['id'] == 0:
            serializer = TaskGroupSerializer(data=operate_data)
            if serializer.is_valid():
                serializer.save()
            elif common.is_serial_id_overflow_errer(serializer.errors):  # 数据库存储的是无符号64位整型数据，django模型BigIntegerField不支持无符号64位，所以rest-framework序列化时对于比有符号最大值还大的数会报错，这是采用django model的原生create入库
                TaskGroup.objects.create(**operate_data)
            else:
                return common.ui_message_response(400, json.dumps(serializer.errors), '数据缺失或字段不符合规定，序列化出错')
        else:
            TaskGroup.objects.filter(id=data['id']).update(**operate_data)
        common.generate_system_log(request_data, u'任务组操作', u'添加任务组',
                                   u'添加任务组' + json.dumps(operate_data))
        return common.ui_message_response(200, '增加成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'任务组操作', u'添加任务组',
                                   u'添加任务组' + json.dumps(operate_data)+u'添加任务组模块异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 批量删除任务组
def delete_taskgroup(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        id_list = common.check_request_list_or_dict_field(request_data, 'id')
        if isinstance(id_list, Response):
            return id_list

        TaskGroup.objects.filter(id__in=id_list).delete()  # 删除
        common.generate_system_log(request_data, u'任务组操作', u'批量删除任务组',
                                   u'批量删除任务组：'+request_data.get('id'))
        return common.ui_message_response(200, '删除成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'任务组操作', u'批量删除任务组',
                                   u'批量删除任务组：' + request_data.get('id')+u'模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 批量修改任务组
def update_batch_taskgroup(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        update_terms = {}
        name = request_data.get('name')
        remarks = request_data.get('remarks')
        if name is not None:
            update_terms['name'] = name
        if remarks is not None:
            update_terms['remarks'] = remarks
        id_list = common.check_request_list_or_dict_field(request_data, 'id')
        if isinstance(id_list, Response):
            return id_list

        TaskGroup.objects.filter(id__in=id_list).update(**update_terms)  # 更新
        common.generate_system_log(request_data, u'任务组操作', u'批量修改任务组',
                                   u'批量修改任务组：' + request_data.get('id'))
        return common.ui_message_response(200, '修改成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'任务组操作', u'批量修改任务组',
                                   u'批量修改任务组：' + request_data.get('id')+u'模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


