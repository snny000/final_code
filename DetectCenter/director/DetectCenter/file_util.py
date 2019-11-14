# -*- coding: utf-8 -*-
import os
import datetime
import time
import threading

mutexes = {}   # 创建一个文件-锁的字典


# 将字符串追加写入文件
def string2file(content, path="../log/", name="access.log"):
    """
    将字符串追加写入文件
    :param content: 需要写入的字符串内容
    :param path:    文件的位置（不包括文件名）
    :param name:    文件名
    :return:
    """
    filename = path + name
    if filename in mutexes:
        mu = mutexes[filename]
    else:
        mu = threading.Lock()
        mutexes[filename] = mu

    if mu.acquire(True):   # 获取锁状态
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception:
            print "路径已被创建"
        if os.path.exists(filename):
            fp = open(filename, 'a+')
        else:
            try:
                os.mknod(filename)
            except Exception:
                print "文件已被创建"
            fp = open(filename, 'a+')
        try:
            fp.write(content + '\n')
            fp.flush()
        except:
            print "write error"
        finally:
            fp.close()
            mu.release()  # 释放锁


# 将字符串追加写入文件，文件名由当天日期自动生成，形式为：“prifix + date + suffix”
def string2log_append_per_day(content, path="../log/", prefix="access", suffix="log"):
    """
    将字符串覆盖写入文件，文件名由当天日期自动生成，形式为：“prifix + date + suffix”
    :param content:   需要写入的字符串内容
    :param path:      文件的位置（不包括文件名）
    :param prefix:    文件名的前缀，一般用于在日期前说明记录的文件的内容关键字
    :param suffix:    文件名的后缀，即文件类型，无需使用‘.’号
    :return:
    """
    date = time.strftime('%Y%m%d', time.localtime())
    name = prefix + date + '.' + suffix
    content = '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '] ' + content
    string2file(content, path, name)


# 将字符串追加写入文件，路径（通过sub_dir_grading指定目录的粒度：年、月、日，默认是日）和文件名由当天日期自动生成，路径形式为：“path/sub_dir”，文件名形式为：“prifix + date + suffix”
def string2log_append_per_day_with_sub_dir(content, path="../log/", prefix="access", suffix="log", sub_dir_grading=2):
    """
    将字符串追加写入文件，路径（通过sub_dir_grading指定目录的粒度：年、月、日，默认是日）和文件名由当天日期自动生成，路径形式为：“path/sub_dir”，文件名形式为：“prifix + date + suffix”
    :param content:   需要写入的字符串内容
    :param path:      文件的位置（不包括文件名）
    :param prefix:    文件名的前缀，一般用于在日期前说明记录的文件的内容关键字
    :param suffix:    文件名的后缀，即文件类型，无需使用‘.’号
    :param sub_dir_grading:  追加子目录粒度  0: 年 1: 月 2: 日
    :return:
    """
    new_path = path + get_sub_dir(sub_dir_grading)
    date = time.strftime('%Y%m%d', time.localtime())
    name = prefix + date + '.' + suffix
    content = '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '] ' + content
    string2file(content, new_path, name)


# 通过时间构建存储文件的相对子目录
def get_sub_dir(grading=3):
    """
    根据给定粒度获取相对子目录
    grading-> 0: 年/ 1: 年/月/ 2: 年月/日/ 3: 年/月/日/
    :param grading:  粒度  0: 年 1: 月 2: 日
    :return:   grading-> 0: 年/ 1: 年/月/ 2: 年月/日/ 3: 年/月/日/
    """
    str_format = '%Y/%m/%d/'
    if grading == 0:
        str_format = '%Y/'
    elif grading == 1:
        str_format = '%Y/%m/'
    elif grading == 2:
        str_format = '%Y%m/%d/'
    sub_dir = time.strftime(str_format, time.localtime(time.time()))  # 文件存储相对路径的子目录
    return sub_dir


# 从文件的offset位置读取length长度字符，默认读取全部
def read_file(file_path, offset=0, length=-1):
    f = open(file_path, 'rb')
    f.seek(offset)
    data = f.read(length)
    f.close()
    return data


# 文件上传，保存在服务器上
def handle_upload_file(absolute_path, f, save_name=''):
    """
    将上传文件保存本地
    :param absolute_path:  绝对路径
    :param f:              上传的文件
    :param save_name:      存储的文件名
    :return:               成功：True 失败：False
    """
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)
    if save_name != '':
        file_name = os.path.join(absolute_path, save_name)
    else:
        file_name = os.path.join(absolute_path, f.name)
    if os.path.exists(file_name):
        return False
    else:
        file_save = open(file_name, 'wb')
        for chunk in f.chunks():
            file_save.write(chunk)
        # for line in f:
        #     file_save.write(line)
        file_save.close()
        return True


# 文件下载，保存在服务器上
def handle_download_file(absolute_path, r, save_name=''):
    """
    将上传文件保存本地
    :param absolute_path:  绝对路径
    :param r:              文件响应
    :param save_name:      存储的文件名
    :return:               成功：True 失败：False
    """
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)
    file_name = os.path.join(absolute_path, save_name)
    # if os.path.exists(file_name):
    #     return False
    # else:
    #     with open(file_name, 'wb') as fd:
    #         for chunk in r.iter_content(1024):
    #             fd.write(chunk)
    #     return True
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(1024):
            fd.write(chunk)
    return True

