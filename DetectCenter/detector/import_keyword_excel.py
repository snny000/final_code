# -*- coding:utf-8 -*-
import time
import xlrd
import copy
import traceback
import os
import sys
import django
from imconfig.models import *

pathname = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DetectCenter.settings")

django.setup()

def import_keyword(file_path):
    try:
        if not os.path.exists(file_path):
            print '文件不存在'
            return

        default_field_value = {
            #"rule_id"：数据库自增
            "rule_type": 1,
            #"rule_cont"：关键词内容
            "rule_mode": 0,
            "rule_level": 100,
            "rule_oprator": 0,
            #"rule_confirm_time":不需要
            #"rule_delete_time":不需要
            "rule_add_date": time.time(),
            #"rule_mod_date":不需要
            "reserve_1": 1,
            #"reserve_2":子类型名称
            "rule_sub_type": 0,
            #"rule_operate_comment":操作备注
        }

        try:
            book = xlrd.open_workbook(file_path)
        except:
            print '文件格式不是xls或xlsx格式'
            return
        sheet = book.sheet_by_index(0)
        first_row = sheet.row_values(0)
        rows_num = sheet.nrows
        cols_num = sheet.ncols
        for i in xrange(1, rows_num):
            for j in range(cols_num):
                default_field_value[first_row[j]] = sheet.cell_value(i, j)
            print '************', default_field_value
            keyword_rule = MB_Rule_Keyword(**(copy.deepcopy(default_field_value)))
            keyword_rule.save()
    except Exception:
        traceback.print_exc()

# 在这里设置文件路径
file_path = ''
import_keyword(file_path)
