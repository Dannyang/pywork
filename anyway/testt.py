# coding=utf-8

import base64
import hashlib
import json
import uuid
from urllib.parse import unquote

import requests

import token_const


def sendmyrequest():
    Token = token_const.UserInfoCheng()
    host = token_const.HostTest().hostAddr
    username = Token.username
    password = Token.password
    url = host + '/dream/app/api-user/verify-code/img'  # 替换为你的目标URL
    # 定义查询字符串参数
    version = {"protocolVersion": "0.0.0"}
    response = requests.get(url, params=version)
    if response.status_code == 200:
        response_json = response.json()
        # 将解码后的字节数据转换为字符串
        verificationCode = base64.b64decode(response_json['data']['verificationCode']).decode('utf-8')
        # print(verificationCode)
        verificationCodeKey = response_json['data']['verificationCodeKey']
        url_1 = host + '/dream/app/api-user/login/username-pwd'
        # data = {'key1': 'value1', 'key2': 'value2'}  # 请求的数据
        machineCode = str(uuid.uuid4())
        data = {"username": username, "password": hashlib.md5(password.encode()).hexdigest(), "appVersion": "1.0.0",
                "verificationCode": verificationCode, "verificationCodeKey": verificationCodeKey,
                "machineCode": machineCode}
        # print(json.dumps(data))
        # 定义请求头，包含JSON格式的内容
        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        # data是dict类型需要使用json.dumps方法将其转为json类型
        response_1 = requests.post(url_1, params=version, data=json.dumps(data), headers=headers)
        if response_1.status_code == 200:
            response_json_1 = response_1.json()
            try:
                Token.token = response_json_1['data']['token']
                print(response_json_1['data']['token'])
                write_token(username, response_json_1['data']['token'])
            except Exception as e:
                # 捕获并处理任何异常
                print(f"发生了异常: {e}")
                input("按 Enter 键退出...")
        else:
            print(f'response_json_1 error')
    else:
        print('error')


def write_token(username, new_token):
    with open('token.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # print(data)
        old_token = data.get(username)
    if old_token is not None:
        data[username] = new_token
        with open('token.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)  # indent=4 用于美化 JSON 文件
        print("done")


def my_decrypt(encode_str):
    if not encode_str:
        return ''
    else:
        length = len(encode_str)
        if length >= 20:
            start = encode_str[:10]
            body = encode_str[10:-10]
            end = encode_str[-10:]
            encode_str = end + body + start
    # 翻转字符串前后顺序
    encode_str = encode_str[::-1]
    # Base64解码
    decode_str = base64.b64decode(encode_str).decode('utf-8')
    return unquote(decode_str, 'utf-8').replace('+', '%2B')
    # decode_str = base64.b64decode(encode_str).decode('utf-8').replace('+', '%2B')


if __name__ == '__main__':
    sendmyrequest()
    # str = "2YyITJCdTJTJ4QjYjdTYjNzNiJWOyUTO5cDZ0QDNlVTZiFWMiRmNzUjMyUSQzUiMyUSeltUZk92Qu9Wa0F2YpZWayVmdyITJDJTJyITJENTJENTJnllMsdkWyITJBNTJyITJlR2bD52bpRXYjlmZpJXZ2JjMlI0NlE0MlIjMlEGdhRmMyUyQyUCbsVnbBNTJyITJldWYzNXZtJjMlMkMlATQzUiMyUSZk9EdTJEdTJyI"
    # print(my_decrypt(str))
