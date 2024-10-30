from telnetlib import EC

import requests
import json

import ddddocr  # 导入 ddddocr
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExecCond  # 正确导入


# # 模拟接口请求
# url = 'https://jsbt.asfsg.com/api/game/role-list'
# form_data = {
#     'serverID': '1',  # 假设你想使用选中的值作为 serverID
#     'account': '13677912846'
# }
#
# # 发送 POST 请求
# response = requests.post(url, data=form_data)
#
# # 输出接口返回值
# print('API Response:', response.json())

def verify(img_code):
    img_code.screenshot('verifyCode.png')
    ocr = ddddocr.DdddOcr(show_ad=False)  # 实例化
    with open('verifyCode.png', 'rb') as f:  # 打开图片
        img_bytes = f.read()  # 读取图片
        res = ocr.classification(img_bytes)  # 识别
        return res


def my_cdk(server, my_account):
    driver = webdriver.Chrome()
    driver.get('https://jsbt.asfsg.com/index/cdk')
    server_element = driver.find_element(By.ID, 'server')
    # 创建 Select 对象
    select = Select(server_element)
    # 获取选中的值
    time.sleep(1)
    select.select_by_value(server)
    account = driver.find_element(By.ID, 'account')
    account.send_keys(my_account)
    button = driver.find_element(By.ID, 'getRoleList')
    button.click()
    time.sleep(5)
    roles_element = driver.find_element(By.ID, 'roles')
    # 创建 Select 对象
    roles = Select(roles_element)
    roles.select_by_index(1)
    cdk = driver.find_element(By.ID, 'cdk')
    cdk.send_keys('js2024666')
    imgCode = driver.find_element(By.ID, 'verifyCode')
    the_captcha = verify(imgCode)
    captcha = driver.find_element(By.ID, 'captcha')
    captcha.send_keys(the_captcha)
    SubmitBtn = driver.find_element(By.ID, 'SubmitBtn')
    SubmitBtn.click()
    # 显式等待，直到 modal-body 元素可见
    modal_body_element = WebDriverWait(driver, 10).until(
        ExecCond.visibility_of_element_located((By.CLASS_NAME, 'modal-body'))
    )
    # 获取文本内容
    modal_text = modal_body_element.text
    if '验证码错误' in modal_text:
        driver.quit()
        return my_cdk(server, my_account)
    time.sleep(3)
    driver.quit()


my_cdk('1', '13677912846')
my_cdk('3', '13677912846')
my_cdk('1', '15847134416')
my_cdk('3', '15847134416')
print("全部领取完成")
