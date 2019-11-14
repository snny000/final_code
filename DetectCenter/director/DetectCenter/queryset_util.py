# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet
import json
import datetime


class CJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		else:
			return json.JSONEncoder.default(self, obj)


'''
作用：
    将queryset转化为json字符串
参数：
    queryset：数据库查询的queryset结果
    fields：需要保留的字段名的集合
    excludes：需要排除的字段名的集合
返回值：
    查询结果的json字符串
注意事项：
    excludes参数存在时fields参数无效
'''


def get_json_of_queryset(queryset, fields=(), excludes=()):
	if not queryset.exists():
		return '[]'
	if excludes:
		fields = set(queryset.values()[0].keys()) - set(excludes)
	lst = list(queryset.values(*fields))
	return json.dumps(lst, cls=CJsonEncoder, encoding='utf-8')


'''
作用：
    将queryset转化为list对象
参数：
    queryset：数据库查询的queryset结果
    fields：需要保留的字段名的集合
    excludes：需要排除的字段名的集合
返回值：
    查询结果的list对象
注意事项：
    excludes参数存在时fields参数无效
'''


def get_list_of_queryset(queryset, fields=(), excludes=(), time_serialize=1):
	if not queryset.exists():
		return []
	if excludes:
		fields = set(queryset.values()[0].keys()) - set(excludes)
	lst = list(queryset.values(*fields))
	if time_serialize:
		s = json.dumps(lst, cls=CJsonEncoder, encoding='utf-8')
		return json.loads(s, encoding='utf-8')
	else:
		return lst


'''
作用：
    将queryset转化为dict对象
参数：
    queryset：数据库查询的queryset结果
    key_fields：需要作为字典key值的字段名
    values_fields：需要作为字典values值的字段名
返回值：
    查询结果的dict对象
'''


def get_dict_of_queryset(queryset, key_field='id', values_field=None):
	if not queryset.exists():
		return {}
	lst = list(queryset.values())
	if not (lst[0].has_key(key_field) and lst[0].has_key(values_field)):
		return {}
	dic = {}
	for d in lst:
		key = d[key_field]
		value = d[values_field]
		dic[key] = value
	return dic


'''
作用：
    获取界面显示每页起始条目和每页条数
参数：
    request_para：请求中的参数
返回值：
    三元组:(起始数据位置， 末尾数据位置， 每页条数)
'''


def get_page_data(request_para):
	page_num = int(request_para.get('pn', 1))  # 页码，默认为第一页
	page_size = int(request_para.get('p_size', 10))  # 每页条数，默认为10

	start_pos = (page_num - 1) * page_size  # 每页起始条码
	end_pos = page_num * page_size  # 每页结束条码

	return start_pos, end_pos, page_size
