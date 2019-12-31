# -*- coding: utf-8 -*-

###############################################################################


#configuration files

#database path and name
db = 'ondb.db'

#define mac
mac_jf = '8888-8888-8888' #jufang
mac_cj = '6666-6666-6666' #changjia
mac_in = 'aaaa-aaaa-aaaa' #infrastructure

#!!!gateway must be the first one!!!
#only support H3C, Cisco and Raisecom
objs = [
    {'type': 'H3C', 'ip': '10.4.101.254', 'port': 23, 'username': 'jianren', 'password': 'jianren123!@#', 'enpassword': None}, #gateway
    {'type': 'Cisco', 'ip': '10.4.101.234', 'port': 23, 'username': None, 'password': 'cisco', 'enpassword': 'jianren123!@#'}, #2f-s-1
    {'type': 'Cisco', 'ip': '10.4.101.235', 'port': 23, 'username': None, 'password': 'cisco', 'enpassword': 'jianren123!@#'}, #2f-s-2
    {'type': 'Cisco', 'ip': '10.4.101.236', 'port': 23, 'username': None, 'password': 'cisco', 'enpassword': 'jianren123!@#'}, #2f-s-3
    {'type': 'Cisco', 'ip': '10.4.101.240', 'port': 23, 'username': None, 'password': 'cisco', 'enpassword': 'jianren123!@#'}, #2f-n-1
    {'type': 'Cisco', 'ip': '10.4.101.239', 'port': 23, 'username': None, 'password': 'cisco', 'enpassword': 'jianren123!@#'}, #2f-n-2
    {'type': 'Cisco', 'ip': '10.4.101.238', 'port': 23, 'username': None, 'password': 'cisco', 'enpassword': 'jianren123!@#'}, #2f-n-3
    {'type': 'Cisco', 'ip': '10.4.101.229', 'port': 23, 'username': None, 'password': 'cisco', 'enpassword': 'jianren123!@#'}, #4f-s-1
    {'type': 'Cisco', 'ip': '10.4.101.230', 'port': 23, 'username': None, 'password': 'cisco', 'enpassword': 'jianren123!@#'}, #4f-s-2
    {'type': 'Cisco', 'ip': '10.4.101.231', 'port': 23, 'username': None, 'password': 'cisco', 'enpassword': 'jianren123!@#'}, #4f-s-3
    {'type': 'Raisecom', 'ip': '10.4.101.228', 'port': 23, 'username': 'raisecom', 'password': 'raisecom', 'enpassword': None}] #4f-s-4

#reserved IP used for building infrastructure.
reserved_ip = ['10.4.101.225', '10.4.101.226', '10.4.101.242']
for obj in objs: reserved_ip.append(obj.get('ip'))

#department
dept = ['政企及海外业务支撑室', '公众及创新业务支撑室', '计费运营室', 'OSS运营室', 'IT服务响应室', '销售品运营室', '规则与流程运营室', '政企及海外业务支撑室厂家', '公众及创新业务支撑室厂家', '计费运营室厂家', 'OSS运营室厂家', 'IT服务响应室厂家', '销售品运营室厂家', '规则与流程运营室厂家']
