# -*- coding: utf-8 -*-

device_statusMap = {
    0: '未接入指挥中心',
    1: '认证成功',
    2: '暂未审核',
    3: '审核失败',
    4: '审核成功',
    5: '认证失败',
    6: '待注册',
}

director_host = '219.143.226.100'    # 指挥中心传输ip

detect_center_host = '219.143.226.98'  # 管理中心IP

ip_whitelist = ['219.143.226.100', '172.17.0.1']  # 管理中心连接指挥节点后允许接收指挥下行数据的IP白名单

# 管理中心编号和上层指挥节点编号
SRC_CENTER_ID = '180206020006'
SRC_NODE = 'GJ536870915'

SOFT_VERSION = '20180209_1234'
ORGANS = 'iie'
DEVICE_CA = 'iie'
ADDRESS = '北京市海淀区闵庄路甲89号'
ADDRESS_CODE = '100000'
CENTER_USER_AGENT = SRC_CENTER_ID + '/' + SOFT_VERSION + '(' + ORGANS + ')'

CENTER_SERIAL = '536870924'   # 管理中心所在行政地区唯一编码，用户生成策略ID、任务组ID和各种任务ID做拼接

CENTER_COOKIE = None

# 发送给指挥系统的URL
DIRECTOR_URL = 'https://' + director_host + ':443/V1/jcc/data'

send_director_A = 'https://' + director_host + ':443/V1/jcc/'

import os
from DetectCenter.settings import BASE_DIR

# 证书路径（CA根证书、客户端证书、客户端私钥）
# 回传指挥中心的证书路径配置
CA_CRT_PATH = BASE_DIR + '/certificates/private/ca.crt'
CLIENT_CRT_PATH = BASE_DIR + '/certificates/server/server.crt'
CLIENT_KEY_PATH = BASE_DIR + '/certificates/server/server.key'

reg_auth_heartbeat_header = {
    'Src-Node': SRC_NODE,
    'Src-Center': SRC_CENTER_ID,
    'Content-Type': 'application/json',
    'Channel-Type': 'JCQ',
    'X-Forwarded-For': detect_center_host
}
