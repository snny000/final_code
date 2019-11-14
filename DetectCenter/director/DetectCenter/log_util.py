# -*- coding: utf-8 -*-
"""
Created on Mon Oct 9 10:38:29 2017

@author: Mirror
"""
import date_util as du


# def make_log_str(header):
# 	remote_addr = header.get('Remote-Addr', '')
# 	strTime = tu.get_current_date_string()  ###获得默认格式的时间字符串
# 	content_length = header.get('Content-Length')
# 	content_type = header.get('Content-Type', '')
# 	request_method = header.get('Request-Method', '')
# 	path_info = header.get('Path-Info', '')
# 	server_protocol = header.get('Server-Protocol', '')
# 	if len(content_length) == 0:
# 		content_length = '0'
# 	####request.scheme
# 	log_str = remote_addr + ' [' + strTime + '] ' + request_method + ' ' + path_info + ' ' + server_protocol + ' ' + content_type + ' ' + str(content_length)
# 	return log_str


def make_log_str_from_request(req):
	# request_header = sender.get_header_from_request(request.META)
	remote_addr = req.META.get('REMOTE_ADDR', '0.0.0.0')
	x_remote_addr = req.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0')   #####源头地址
	# req.META['REMOTE_ADDR'] = remote_addr
	strTime = du.get_current_date_string()
	content_length = req.META.get('CONTENT_LENGTH', '0')
	# print 'content_length:', '=' + content_length + '='
	if len(content_length) == 0:
		content_length = '0'
	content_type = req.META.get('CONTENT_TYPE', 'NULL')
	server_protocol = req.META.get('SERVER_PROTOCOL', 'UNKOWN')
	####request.scheme
	log_str = x_remote_addr + ' ' + remote_addr + ' [' + strTime + '] ' + req.method + ' ' + req.path + ' ' + server_protocol + ' ' + content_type + ' ' + content_length

	return log_str


def make_log_str_from_response(resp):
	url = resp.url
	remote_addr = resp.request.headers.get('Remote-Addr', '0.0.0.0')
	x_remote_addr = resp.request.headers.get('X-Remote-Addr', remote_addr)   #####源头地址

	url_lst = url.split('/')
	dst_addr = url_lst[2].split(':')[0]
	if len(dst_addr) < 7:
		dst_addr = '0.0.0.0'

	strTime = du.get_current_date_string()
	method = resp.request.method
	path = ''
	for s in url_lst[3:]:
		path += '/' + s
	# server_protocol = url_lst[0][:-1].upper()
	if url_lst[0] == 'http:':
		server_protocol = 'HTTP/1.1'
	elif url_lst[0] == 'https:':
		server_protocol = 'HTTPS/1.1'
	else:
		server_protocol = 'UNKOWN'
	content_length = resp.headers.get('Content-Length', '')
	if len(content_length) == 0:
		content_length = '0'
	content_type = resp.headers.get('Content-Type', 'NULL').split(';')[0]
	####request.scheme
	log_str = x_remote_addr + ' ' + dst_addr + ' [' + strTime + '] ' + method + ' ' + path + ' ' + server_protocol + ' ' + content_type + ' ' + content_length + ' ' + str(resp.status_code)
	return log_str


def http_error_log():
	log_str = '0.0.0.0 [%s] NULL NULL NULL NULL -1 000' % (du.get_current_date_string())
	return log_str
