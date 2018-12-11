# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     alarm_query
   Description :
   Author :       Lychlov
   date：          2018/12/5
-------------------------------------------------
   Change Activity:
                   2018/12/5:
-------------------------------------------------
"""
import json
import requests
import uuid

from .base_conf import ALARM_BASE_URL, BASE_STATION_QUIT, CELL_QUIT,LINE_LIMIT

def old_alarm_query(content):
    QUERY_FUNS = {'101': query_101,
                  '102': query_102,
                  '103': query_103,
                  '104': query_104,
                  '105': query_105,
                  '106': query_106,
                  '107': query_107}
    content = content.replace('，', ',')
    parts = content.split(',')
    if len(parts) > 1:
        query_type = parts[0]
        query_para = parts[1]
    else:
        query_type = parts[0]
        query_para = None
    try:
        query_fun = QUERY_FUNS[query_type]
    except:
        return '查询指令有误，请参照说明。'
    return query_fun(query_para)


def query_101(zone=None):
    paras = {'sessionid': uuid.uuid1(),
             'device_city': '南阳市',
             'page': 1,
             'limit': LINE_LIMIT,
             }
    if zone:
        paras['device_county'] = zone
    response = requests.get(url=ALARM_BASE_URL, params=paras)
    result = json.loads(response.content.decode())
    return parse_101(result)


def query_102(cell_id=None):
    if cell_id is None:
        return '支持的格式为"102，基站号",请重试。'
    paras = {'sessionid': uuid.uuid1(), 'device_city': '南阳市', 'page': 1, 'limit': LINE_LIMIT, 'property11': cell_id}
    response = requests.get(url=ALARM_BASE_URL, params=paras)
    result = json.loads(response.content.decode())
    return parse_101(result)


def query_103(alarm_id=None):
    if alarm_id is None:
        return '支持的格式为"103，网管告警ID",请重试。'
    paras = {'sessionid': uuid.uuid1(), 'device_city': '南阳市', 'page': 1, 'limit': LINE_LIMIT, 'event_id': alarm_id}
    response = requests.get(url=ALARM_BASE_URL, params=paras)
    result = json.loads(response.content.decode())
    return parse_101(result)


def query_104(ci=None):
    if ci is None:
        return '支持的格式为"104，小区CI",请重试。'
    paras = {'sessionid': uuid.uuid1(), 'device_city': '南阳市', 'page': 1, 'limit': LINE_LIMIT, 'property9': ci}
    response = requests.get(url=ALARM_BASE_URL, params=paras)
    result = json.loads(response.content.decode())
    return parse_101(result)


def query_105(zone=None):
    paras = {'sessionid': uuid.uuid1(), 'device_city': '南阳市', 'page': 1, 'limit': LINE_LIMIT, 'event_id': CELL_QUIT}
    if zone:
        paras['device_county'] = zone
    response = requests.get(url=ALARM_BASE_URL, params=paras)
    result = json.loads(response.content.decode())
    return parse_101(result)


def query_106(zone=None):
    paras = {'sessionid': uuid.uuid1(), 'device_city': '南阳市', 'page': 1, 'limit': LINE_LIMIT, 'event_id': BASE_STATION_QUIT}
    if zone:
        paras['device_county'] = zone
    response = requests.get(url=ALARM_BASE_URL, params=paras)
    result = json.loads(response.content.decode())
    return parse_101(result)


def query_107(zone=None):
    paras = {'sessionid': uuid.uuid1(), 'device_city': '南阳市', 'page': 1, 'limit': LINE_LIMIT, 'vendor_event_id': '92001'}
    if zone:
        paras['device_county'] = zone
    response = requests.get(url=ALARM_BASE_URL, params=paras)
    result = json.loads(response.content.decode())
    return parse_101(result)


def parse_101(result):
    parsed = "序号|网元名称|所属区县|设备厂家|告警发生时间|厂家告警号|告警中文名|告警对象名称|基站编号\n";
    index = 1
    for item in result:
        parsed += str(index) + "|" + item.get("device_name") + "|" + item.get("device_county") + "|" + item.get(
            "device_vendor") + "|" + item.get("last_time") + "|" + item.get("vendor_event_id") + "|" + item.get(
            "title") + "|" + item.get("object_name") + "|" + str(item.get("property11")) + "\n"
        index += 1
    return parsed
