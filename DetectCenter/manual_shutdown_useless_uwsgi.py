# -*- coding: utf-8 -*-

import time
import subprocess
import traceback
from datetime import datetime, timedelta
import json
import os

# 清除工程运行过程中产生的uwsgi僵尸进程
def shutdown_useless_uwsgi_process():

    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ": 开始清除僵尸进程..."
    p_count_cmd = 'ps -eo pid,ppid,stat,args | grep uwsgi | grep -v grep | wc -l'
    p_count_res = json.loads(exce_sync_shell_command(p_count_cmd), encoding='utf-8')
    print "总进程数: ", p_count_res["data"].strip()
    if int(p_count_res["data"]) > 1:
        # parent_p_cmd = "ps -eo pid,ppid,stat,args | grep uwsgi | grep -v grep | awk '{print $1\",\"$2}'"
        # parent_p_res = json.loads(exce_sync_shell_command(parent_p_cmd), encoding='utf-8')
        # pid_list = []
        # ppid_dict = {}
        # ll = parent_p_res["data"].strip().split("\n")
        # for var in ll:
        #     if var.strip() == "":
        #         continue
        #     tmp = var.split(",")
        #     if not tmp[0].strip() == "":
        #         pid_list.append(int(tmp[0]))
        #     if not tmp[1].strip() == "":
        #         if int(tmp[1]) in ppid_dict:
        #             ppid_dict[int(tmp[1])] = ppid_dict[int(tmp[1])] + 1
        #         else:
        #             ppid_dict[int(tmp[1])] = 1
        # sorted_dict_list = sorted(ppid_dict.items(), key=lambda x: x[1], reverse=True)
        # parent_p_pid = 0
        # for var in sorted_dict_list:
        #     if not var[0] == 1 and var[0] in pid_list:
        #         parent_p_pid = var[0]
        #         break

        pathname = os.path.dirname(os.path.abspath(__file__))
        pid_path = os.path.join(pathname, 'running/uwsgi.pid')
        print "父进程ID存储文件路径: ", pid_path
        parent_p_cmd = "cat " + pid_path
        parent_p_res = json.loads(exce_sync_shell_command(parent_p_cmd), encoding='utf-8')
        parent_p_pid = parent_p_res["data"].strip()
        print "父进程ID: ", parent_p_pid
        all_p_cmd = "ps -eo pid,ppid,stat,args | grep uwsgi | grep -v grep | awk '{print $1\",\"$2\",\"$3}'"
        all_p_res = json.loads(exce_sync_shell_command(all_p_cmd), encoding='utf-8')
        process_list = all_p_res["data"].split("\n")
        z_count = 0
        for var in process_list:
            if var.strip() == "":
                continue
            single_p_list = var.strip().split(",")
            if single_p_list[2] == "Z" or single_p_list[2] == "z" or (single_p_list[1] == "1" and not single_p_list[0] == str(parent_p_pid) and (not single_p_list[2] == "R" and not single_p_list[2] == "r")):
                json.loads(exce_sync_shell_command("kill -9 " + single_p_list[0]), encoding='utf-8')
                z_count += 1
                print "杀死僵尸进程->id,pid,stat: ", var
                time.sleep(1/1000)
            else:
                pass
        print "一共清除僵尸进程数: ", z_count
    print '\n'


def constructCommand(command):
    if isinstance(command, list):
        return '\n'.join(command)
    else:
        return command


'''
功能：
    执行含有像tail这种不会立刻返回的shell命令
参数：
    command：要执行的shell命令
    read_seconds: 设置command执行的时间，单位秒
    sleep_time：每次获取command返回码后的休眠时间
返回值：
    result = {
        "data": "",  command执行结果
        "err": "",   command执行的错误信息
        "code": 1    函数执行结果, 1:正常 0:异常
    } json串
注意事项：
    sleep_time应该小于read_seconds
'''
def exce_async_shell_command(command, read_seconds=5, sleep_time=0.1):

    result = {
        "data": "",
        "code": 1,
        "err": ""
    }
    _command = constructCommand(command)
    subp = None
    try:
        result_list = list()
        ss = ""
        subp = subprocess.Popen([_command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        read_to_time = (datetime.now() + timedelta(seconds=read_seconds)).strftime('%Y-%m-%d %H:%M:%S')
        read_to_timestamp = time.mktime(time.strptime(read_to_time, '%Y-%m-%d %H:%M:%S'))
        print read_to_time, read_to_timestamp
        while subp.poll() == None:
            # result_list.append(subp.stdout.readline().replace("\n", ""))
            if time.mktime(time.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')) > read_to_timestamp:
                break
            time.sleep(sleep_time)
            # print "Command:", _command, "return code:", subp.returncode
            # result["data"] = "\n".join(result_list)
    except Exception:
        traceback.print_exc()
        result["code"] = 0
    finally:
        if subp.poll() == None:
            subp.terminate()        # 对于像tail不会主动结束的命令，如果不显示停止子进程，stdout和stderr的read()方法会一直阻塞主进程
            subp.kill()
        result["data"] = subp.stdout.read()
        result["err"] = subp.stderr.read()
        return json.dumps(result, ensure_ascii=False, encoding='utf-8')


'''
功能：
    执行立刻返回的shell命令, 不含有像tail这种命令
参数：
    command：要执行的shell命令，可以为list或者str，如果是str多条命令用\n隔开
返回值：
    result = {
        "data": "",  command执行结果
        "err": "",   command执行的错误信息
        "code": 1    函数执行结果, 1:正常 0:异常
    } json串
注意事项：
'''
def exce_sync_shell_command(command):

    result = {
        "data": "",
        "err": "",
        "code": 1
    }
    try:
        _command = constructCommand(command)
        subp = subprocess.Popen([_command], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        # ss = subp.stdout.read()
        while subp.poll() == None:
            continue
        # print "Command:", _command, "return code:", subp.returncode
        # result['data'] = ss
    except Exception:
        traceback.print_exc()
        result["code"] = 0
    finally:
        if subp.poll() == None:
            subp.terminate()
            subp.kill()
        result["data"] = subp.stdout.read()
        result["err"] = subp.stderr.read()
        return json.dumps(result, ensure_ascii=False, encoding='utf-8')


if __name__ == "__main__":
    shutdown_useless_uwsgi_process()


