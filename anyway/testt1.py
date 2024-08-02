# coding=utf-8
import json

import requests
from url_constant import MyURL
import token_const


def sendmyrequest():
    RequestEnum = MyURL.PARENT_TASKS
    host_addr = token_const.HostLocal().hostAddr
    url = host_addr + RequestEnum.value['url']
    if 'data' in RequestEnum.value:
        data = RequestEnum.value['data']
    else:
        data = None
    if 'param' in RequestEnum.value:
        param = RequestEnum.value['param']
    else:
        param = None
    with open('token.json', 'r') as json_file:
        tokenList = json.load(json_file)
        login_token = tokenList["caowenhao"]
        # 定义查询字符串参数
    headers = {"Login-token": login_token,
               "Content-Type": "application/json;charset=UTF-8"}
    # print(headers)
    response = requests.request(RequestEnum.value['method'], url, params=param, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        content = response.json()
        if content['code'] == 0:
            print(json.dumps(content['data'], indent=4, ensure_ascii=False))
        else:
            print(content['message'])
    else:
        print('error')


if __name__ == '__main__':
    sendmyrequest()
