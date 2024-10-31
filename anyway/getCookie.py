import time

import ddddocr  # 导入 ddddocr
from selenium.webdriver.common.by import By
from seleniumwire import webdriver


def verify(img_code):
    img_code.screenshot('verifyCode.png')
    ocr = ddddocr.DdddOcr(show_ad=False)  # 实例化
    with open('verifyCode.png', 'rb') as f:  # 打开图片
        img_bytes = f.read()  # 读取图片
        res = ocr.classification(img_bytes)  # 识别
        return res


def my_cdk(my_password, my_username, count):
    driver = webdriver.Chrome()
    driver.get('https://dream.mysteelcms.com/portal_login')
    time.sleep(2)
    # 拦截请求
    username = driver.find_element(By.ID, 'username')
    username.send_keys(my_username)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(my_password)
    imgCode = driver.find_element(By.ID, 'kaptchaCode')
    the_captcha = verify(imgCode)
    vCode = driver.find_element(By.ID, 'vCode')
    vCode.send_keys(the_captcha)
    SubmitBtn = driver.find_element(By.CLASS_NAME, 'loginBtn')
    SubmitBtn.click()
    time.sleep(2)
    form_tip_elements = driver.find_elements(By.CLASS_NAME, 'form-tip')
    # 遍历所有元素，查找可见的元素
    for element in form_tip_elements:
        if element.is_displayed():  # 检查元素是否可见
            # 验证码错误重试
            if '验证码错误' in element.text:
                count = count + 1
                print('验证码错误,重试第' + str(count) + '次')
                driver.quit()
                return my_cdk(my_password, my_username, count)
            else:
                break
    # 等待跳转完成
    time.sleep(5)
    for request in driver.requests:
        cookies = request.headers.get('cookie')
        if cookies and 'mysteel_sso_ticket' in cookies:
            print(f"Cookies: {cookies}")
            break
    time.sleep(10)
    driver.quit()


my_cdk('abc123456', 'changlai', 0)
print("全部领取完成")
