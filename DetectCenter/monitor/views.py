# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from data_processing import *
from DetectCenter.common import WARN_MODULE, WARN_TYPE
from DetectCenter import file_util as fu


# ********************************************************************************
#                                                                                *
#                                   与前端交互接口                                 *
#                                                                                *
# ********************************************************************************

sub_dir = fu.get_sub_dir()   # 返回 ‘%Y/%m/%d’ 格式子目录


class TrojanAlarm(APIView):
    """
    木马攻击窃密告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, AlarmTrojanSerializer, WARN_MODULE['alarm'], WARN_TYPE['trojan'],
                                       'JCQ_GJQM', 'JCQ_GJQM_TROJAN')


class TrojanAlarmFile(APIView):
    """
    木马攻击窃密原始报文处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'alarm_trojan/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_GJQM', 'JCQ_GJQM_TROJAN_FILE', 'JCQ_GJQM_TROJAN')


class ExploitAlarm(APIView):
    """
    漏洞利用窃密攻击告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, AlarmAttackSerializer, WARN_MODULE['alarm'], WARN_TYPE['attack'],
                                       'JCQ_GJQM', 'JCQ_GJQM_ATTACK')


class ExploitAlarmFile(APIView):
    """
    漏洞利用窃密攻击原始报文处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'alarm_attack/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_GJQM', 'JCQ_GJQM_ATTACK_FILE', 'JCQ_GJQM_ATTACK')


class MalwareAlarm(APIView):
    """
    恶意程序窃密攻击告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, AlarmMalwareSerializer, WARN_MODULE['alarm'], WARN_TYPE['malware'],
                                       'JCQ_GJQM', 'JCQ_GJQM_MALWARE')


class MalwareAlarmFile(APIView):
    """
    恶意程序窃密攻击原始报文处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'alarm_malware/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_GJQM', 'JCQ_GJQM_MALWARE_FILE', 'JCQ_GJQM_MALWARE')


class OtherAlarm(APIView):
    """
    其他窃密攻击告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, AlarmOtherSerializer, WARN_MODULE['alarm'], WARN_TYPE['other'],
                                       'JCQ_GJQM', 'JCQ_GJQM_OTHER')


class OtherAlarmFile(APIView):
    """
    其他窃密攻击原始报文处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'alarm_other/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_GJQM', 'JCQ_GJQM_OTHER_FILE', 'JCQ_GJQM_OTHER')


class AbnormalAlarm(APIView):
    """
    未知攻击窃密告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, AlarmAbnormalSerializer, WARN_MODULE['abnormal'], WARN_TYPE['abnormal'],
                                       'JCQ_GJQM', 'JCQ_GJQM_ABNORMAL')


class AbnormalAlarmFile(APIView):
    """
    未知攻击窃密告警原始报文处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'abnormal/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_GJQM', 'JCQ_GJQM_ABNORMAL_FILE', 'JCQ_GJQM_ABNORMAL')


class FingerSensitive(APIView):
    """
    密标文件告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_sensitive(request, 'JCQ_CSSM', 'JCQ_CSSM_MB')


class FingerSensitiveFile(APIView):
    """
    密标文件处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'finger_file/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_CSSM', 'JCQ_CSSM_MB_FILE', 'JCQ_CSSM_MB')


class MarkSensitive(APIView):
    """
    标密文件告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_sensitive(request, 'JCQ_CSSM', 'JCQ_CSSM_SENSITIVE')


class MarkSensitiveFile(APIView):
    """
    标密文件处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'sensitive_file/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_CSSM', 'JCQ_CSSM_SENSITIVE_FILE', 'JCQ_CSSM_SENSITIVE')


class KeywordSensitive(APIView):
    """
    关键词告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_sensitive(request, 'JCQ_CSSM', 'JCQ_CSSM_KEYWORD')


class KeywordSensitiveFile(APIView):
    """
    关键词命中文件处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'keyword_file/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_CSSM', 'JCQ_CSSM_KEYWORD_FILE', 'JCQ_CSSM_KEYWORD')


class EncryptionSensitive(APIView):
    """
    加密文件筛选告警处理接口
    """
    def post(self, request, format=None):
        return process_post_data_sensitive(request, 'JCQ_CSSM', 'JCQ_CSSM_FILTEREDENC')


class EncryptionSensitiveFile(APIView):
    """
    加密文件处理接口
    """
    def post(self, request, format=None):
        relative_path = 'encryption_file/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_CSSM', 'JCQ_CSSM_FILTEREDENC_FILE', 'JCQ_CSSM_FILTEREDENC')


class CompressSensitive(APIView):
    """
    压缩文件检测告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_sensitive(request, 'JCQ_CSSM', 'JCQ_CSSM_FILTEREDCOM')


class CompressSensitiveFile(APIView):
    """
    压缩文件处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'compress_file/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_CSSM', 'JCQ_CSSM_FILTEREDCOM_FILE', 'JCQ_CSSM_FILTEREDCOM')


class PictureSensitive(APIView):
    """
    图文文件筛选告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_sensitive(request, 'JCQ_CSSM', 'JCQ_CSSM_FILTEREDPIC')


class PictureSensitiveFile(APIView):
    """
    图文文件处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'picture_file/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_CSSM', 'JCQ_CSSM_FILTEREDPIC_FILE', 'JCQ_CSSM_FILTEREDPIC')


class StyleSensitive(APIView):
    """
    版式文件检测告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_sensitive(request, 'JCQ_CSSM', 'JCQ_CSSM_LAYOUT')


class StyleSensitiveFile(APIView):
    """
    版式文件处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'style_file/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_CSSM', 'JCQ_CSSM_LAYOUT_FILE', 'JCQ_CSSM_LAYOUT')


class IPIntercept(APIView):
    """
    IP侦听告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, TargetInterceptIPSerializer,
                                       WARN_MODULE['object_listen'], WARN_TYPE['intercept_ip'],
                                       'JCQ_MBSJ', 'JCQ_MBSJ_IP')


class IPInterceptFile(APIView):
    """
    IP侦听告警原始报文处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'intercept_ip/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_MBSJ', 'JCQ_MBSJ_IP_FILE', 'JCQ_MBSJ_IP')


class DNSIntercept(APIView):
    """
    域名帧听告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, TargetInterceptDNSSerializer,
                                       WARN_MODULE['object_listen'], WARN_TYPE['intercept_dns'],
                                       'JCQ_MBSJ', 'JCQ_MBSJ_DOMAIN')


class DNSInterceptFile(APIView):
    """
    域名帧听告警原始报文处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'intercept_dns/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_MBSJ', 'JCQ_MBSJ_DOMAIN_FILE', 'JCQ_MBSJ_DOMAIN')


class URLIntercept(APIView):
    """
    URL侦听告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, TargetInterceptURLSerializer,
                                       WARN_MODULE['object_listen'], WARN_TYPE['intercept_url'],
                                       'JCQ_MBSJ', 'JCQ_MBSJ_URL')


class URLInterceptFile(APIView):
    """
    URL侦听原始报文处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'intercept_url/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_MBSJ', 'JCQ_MBSJ_URL_FILE', 'JCQ_MBSJ_URL')


class AccountIntercept(APIView):
    """
    账号侦听告警处理接口.
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, TargetInterceptAccountSerializer,
                                       WARN_MODULE['object_listen'], WARN_TYPE['intercept_account'],
                                       'JCQ_MBSJ', 'JCQ_MBSJ_ACCOUNT')


class AccountInterceptFile(APIView):
    """
    账号侦听原始报文处理接口.
    """
    def post(self, request, format=None):
        relative_path = 'intercept_account/' + sub_dir
        return process_post_file(request, relative_path,
                                 'JCQ_MBSJ', 'JCQ_MBSJ_ACCOUNT_FILE', 'JCQ_MBSJ_ACCOUNT')


class AlarmBlock(APIView):
    """
    阻断告警处理接口
    """
    def post(self, request, format=None):
        return process_post_data_alarm(request, BlockSerializer,
                                       WARN_MODULE['block'], WARN_TYPE['block'],
                                       'JCQ_TXZD', 'JCQ_TXZD_BLOCK')


# ********************************************************************************
#                                                                                *
#                                   与界面交互接口                                 *
#                                                                                *
# ********************************************************************************


class AlarmShow(APIView):
    """
    查询所有告警信息.
    """
    def get(self, request, format=None):
        return show_all_alarm(request)

    def post(self, request, format=None):
        return show_all_alarm(request)


class AlarmCount(APIView):
    """
    查询告警数量.
    """
    def get(self, request, format=None):
        return show_alarm_count(request)

    def post(self, request, format=None):
        return show_alarm_count(request)


class AlarmDetail(APIView):
    """
    查询告警详情.
    """
    def get(self, request, format=None):
        return show_alarm_detail(request)

    def post(self, request, format=None):
        return show_alarm_detail(request)


class AlarmDetailReportExport(APIView):
    """
    告警详情报表导出.
    """
    def get(self, request, format=None):
        return export_alarm_detail_report(request)

    def post(self, request, format=None):
        return export_alarm_detail_report(request)


class ProcessDownloadFile(APIView):
    """
    下载告警原始报文文件.
    """

    def get(self, request, save_path, format=None):
        return common.process_download_file(request, '', save_path)

    def post(self, request, save_path, format=None):
        return common.process_download_file(request, '', save_path)


#新增


class AlarmCountSeveralDays(APIView):
    """
    查询最近若干天（不包括当前日期，默认为30天）的告警数量.
    """

    def get(self, request, format=None):
        return show_alarm_last_days(request)

    def post(self, request, format=None):
        return show_alarm_last_days(request)


class AlarmCountEveryType(APIView):
    """
    查询每种告警类型的数量.
    """

    def get(self, request, format=None):
        return show_alarm_all_types(request)

    def post(self, request, format=None):
        return show_alarm_all_types(request)


class ExportAlarmReport(APIView):
    """
    导出除了以时间为分类聚合的其他统计结果.
    """

    def get(self, request, format=None):
        return export_alarm_report(request)

    def post(self, request, format=None):
        return export_alarm_report(request)


class ExportTimeAlarmReport(APIView):
    """
    时间-告警数量统计报表导出（某一时间段内）.
    """

    def get(self, request, format=None):
        return export_time_alarm_report(request)

    def post(self, request, format=None):
        return export_time_alarm_report(request)


class ExportLastDaysReport(APIView):
    """
    时间-告警数量统计报表导出（最近一段时间内）.
    """

    def get(self, request, format=None):
        return export_last_days_report(request)

    def post(self, request, format=None):
        return export_last_days_report(request)


# class AlarmCountTopSeveralUser(APIView):
#     """
#     查询告警数量最多的若干个个user.
#     """
#     def get(self, request, format=None):
#         return show_alarm_several_users(request, 10)
#
#     def post(self, request, format=None):
#         return show_alarm_several_users(request, 10)

class ShowAlarmBetweenDays(APIView):
    """
    根据时间条件，查询所在时间段内的告警数量.
    """

    def get(self, request, format=None):
        return show_alarm_days(request)

    def post(self, request, format=None):
        return show_alarm_days(request)


class GetStatisticsCount(APIView):
    """
    根据检测器id统计各种策略告警数量
    """

    def get(self, request, format=None):
        return get_statistics_count(request)

    def post(self, request, format=None):
        return get_statistics_count(request)


class ShowAlarmGroup(APIView):
    """
    统计各个任务的告警数量
    """

    def get(self, request, format=None):
        return show_alarm_task(request)

    def post(self, request, format=None):
        return show_alarm_task(request)