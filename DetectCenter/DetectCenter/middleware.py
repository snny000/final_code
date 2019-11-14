# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 13:38:29 2017

@author: Mirror
"""
import date_util as du
import log_util as lu
from django.http import HttpResponse
import traceback
import time
import file_util as fu
import common

try:
	from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
	MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class URLControlMiddleware(MiddlewareMixin):

	def process_request(self, request):
		# 执行视图view之前被调用  返回None 或 HttpResponse

		remote_addr = request.META['HTTP_X_FORWARDED_FOR'] if request.META.has_key('HTTP_X_FORWARDED_FOR') \
			else request.META.get('REMOTE_ADDR', '0.0.0.0')

		server_port = request.META.get('SERVER_PORT', '0')

		request_method = request.method

		request_path = request.path



		if (server_port == '8089' and  request_method == 'GET') or \
			(server_port == '8089' and remote_addr != global_config.MY_NODE_IP):

			#return message_response(400,'非法访问')
			return HttpResponse('开发的程序员已经被打死')
		return None



class SimpleMiddleware(MiddlewareMixin):
	def process_request(self, request):
		# 调用 view 之前的代码
		# print '###请求调用了中间件SimpleMiddleware##'

		return None

	def process_response(self, request, response):
		# 调用 view 之前的代码
		# print '###响应调用了中间件SimpleMiddleware##'
		return response


class RequestsLog(MiddlewareMixin):
	def process_request(self, request):
		# 调用 view 之前的代码
		# print '###请求调用了中间件SimpleMiddleware##'


		print '\nheader:', request.META
		# request_head = request.META
		# print 'data:', request.data
		# print 'method:[', request.method, ']'

		# print 'method:[', request.META['REQUEST_METHOD'], ']'

		try:
			self.start = int(time.time() * 1000)
		except Exception:
			traceback.print_exc()

		if request.META.has_key('HTTP_X_REMOTE_ADDR'):
			# request.META['REMOTE_ADDR'] = request.META['HTTP_X_REMOTE_ADDR']
			pass
		else:
			request.META['HTTP_X_REMOTE_ADDR'] = request.META['REMOTE_ADDR']

		return None

	def process_exception(self, request, exception):
		# print('m2.process_exception')
		######/alidata/Director/log/2017/10/exception20171004.log 非捕获异常，代码有问题，见到就要改，上线后正常这里走不到
		try:
			remote_addr = request.META.get('REMOTE_ADDR')
			strTime = du.get_current_date_string()  ###获得默认格式的时间字符串
			log_str = remote_addr + ' [' + strTime + '] ' + request.method + ' ' + request.path + ' ' + request.scheme + ' ' + str(
				exception)

			fu.string2log_append_per_day_with_sub_dir(log_str, path=common.LOG_PATH + 'center_access_log/',
			                                               prefix='exception')
		except Exception:
			traceback.print_exc()
		return HttpResponse('开发的程序员已经被打死')

	def process_response(self, request, response):
		# 调用 view 之后的代码
		# print '###响应调用了中间件SimpleMiddleware##'

		########/alidata/Director/log/2017/10/request20171004.log  运行时，业务无关，无条件日志，view崩了都不影响日志，不受业务代码影响，捕获异常在这里体现
		try:

			end = int(time.time() * 1000)
			print('Running time: %s Milliseconds' % (end - self.start))  # 其中end-start就是程序运行的时间，单位是毫秒。

			# remote_addr = request.META.get('REMOTE_ADDR')
			# strTime = tu.get_current_date_string()  ###获得默认格式的时间字符串
			# content_length = request.META.get('CONTENT_LENGTH', -1)
			# # print 'content_length:', '=' + content_length + '='
			# if len(content_length) == 0:
			#     content_length = '0'
			# content_type = request.META.get('CONTENT_TYPE')
			# server_protocol = request.META.get('SERVER_PROTOCOL')
			# ####request.scheme
			# log_str = remote_addr + ' [' + strTime + '] ' + request.method + ' ' + request.path + ' ' + server_protocol + ' ' + content_type + ' ' + content_length
			log_str = lu.make_log_str_from_request(request)
			# print log_str
			# print response.status_code, '\n'
			status_code = response.status_code
			runtime = int(end - self.start)
			log_str = log_str + ' ' + str(status_code) + ' ' + str(runtime)
			fu.string2log_append_per_day_with_sub_dir(log_str, path=common.LOG_PATH + 'center_access_log/',
			                                               prefix='request')
			############192.168.120.241 [2017-10-04 19:55:01] POST /msg/router HTTP/1.1 application/json          340         200         60
			############    客户端ip           请求时间                 接口（请求行）    CONTENT_TYPE       CONTENT_LENGTH  响应码      响应时间
			if status_code != 200:
				fu.string2log_append_per_day_with_sub_dir(log_str, path=common.LOG_PATH + 'center_access_log/',
				                                               prefix='fail')
			if runtime > 50:
				fu.string2log_append_per_day_with_sub_dir(log_str, path=common.LOG_PATH + 'center_access_log/',
				                                               prefix='delay')

		except Exception:
			traceback.print_exc()
			# return common.message_response(500, '服务器%s内部处理错误' % (next))

		return response
