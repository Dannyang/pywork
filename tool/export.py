# coding=utf-8
import json
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
from pathlib import Path
import pandas as pd

cookie = 'jrose=830B963768AA9899649B0A43A997D4A2.ans; siteRole=1; roleEnc=FFC61D695BED4B549473FF78515C10AB; source=""; fid=167983; _uid=159598606; _d=1750335363653; UID=159598606; vc3=LXWMc%2FDEh4Y9XK1p%2B1Zo%2F50wUi9BINSJVN2HdxtHtVLB0kCBx9%2BkkNm8ksA77IV7cGJFo4P5644Cw4wk22%2BoLBtePxhEcovlZ2%2BFLxtHmn3SvoXmiMpjiyyCIKwukErmZjEBDla1ZyffqV8AXBJpriY6HU40o2iDH%2FszPIJVkTc%3D2281e0930cbacd7d41dc816cf72dfff9; uf=b2d2c93beefa90dc0e58f5e20478320846deb320366635b8ccd272461f400c99b5bfe39a28794b8dda5173624c47417a8e33962514b70d6eea4a1670a3a8352f7631dba781cdd959f44425e20f927c6b514e370902fb1934fd8d1b9f89f0c1c6a2caeba8547d183ac29d66c7f7238a5b5cb49c9381c6a6cc04df951ef14fa2fbaa24ec2b1e16004711d78d04c58940be2723ac693a7cdca9fd68be96b6183b1ad8eccfb0b782d78cbc73ff002cb6e046f236767cbd7986eaf3d718d572fcfc7c; cx_p_token=c122ebf3d39424484cd5590740b8895d; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIxNTk1OTg2MDYiLCJsb2dpblRpbWUiOjE3NTAzMzUzNjM2NTQsImV4cCI6MTc1MDk0MDE2M30.kn6WUjSZ8ilyfJRfzSNI3Gp6GfhJDK2Mm5k2SUTjsWo; xxtenc=fba95c7cadc0ec909232a3f602a34229; DSSTASH_LOG=C_38-UN_10575-US_159598606-T_1750335363654; spaceFidEnc=21290A09FD51F85261CB74C4F716856B; spaceFid=167983; spaceRoleId=""; tl=1'
headers = {
    'Cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}
# 按分号和空格分割字符串，得到键值对列表
cookies = cookie.split('; ')
# 遍历键值对，找到fid的值
fid = None
for cookie in cookies:
    if cookie.startswith('fid='):
        fid = cookie.split('=', 1)[1]  # 分割一次，避免值中有等号
        break

status_dict = {'1': '已签到', '8': '事假', '9': '迟到', '0': '未签到', '7': '病假', '2': '教师代签', '12': '公假',
               '5': '缺勤', '10': '早退'}
course_list = ['跨境平台运营与管理置顶']
class_list = ['23跨境电商1班', '23跨境电商2班', '23商英2班', '23商英1班']
# course_list = ['数据库应用基础']
# class_list = ['24工业互联3班', '24工业互联2班', '24工业互联1班']
time_limit = 1739548800551


class Course:
    def __init__(self, course_id: str, course_name: str):
        self.course_id = course_id
        self.course_name = course_name


# class Class:
#     def __init__(self, class_id: str, class_name: str):
#         self.class_id = class_id
#         self.class_name = class_name


def request_course_html():
    url = 'https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courselistdata'
    form_data = {
        'courseType': 0
    }
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, data=form_data)
        # 返回响应对象
        extract_course_ids(response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None


def class_by_course(course):
    url = 'https://mobilelearn.chaoxing.com/v2/apis/class/getClassList'
    param = {
        'fid': fid,
        'courseId': course.course_id
    }
    # 构建完整URL
    url = f"{url}?{urlencode(param)}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查HTTP错误

        # 解析JSON响应（已经解析为字典，无需再次使用json.loads()）
        data = response.json()
        if data.get('result') == 1:
            return data['data']
        else:
            print(f"API请求失败: {data.get('msg', '未知错误')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None


def activity_course_class(course_id, class_id):
    url = 'https://mobilelearn.chaoxing.com/v2/apis/active/pcActivelist'
    param = {
        'fid': fid,
        'courseId': course_id,
        'classId': class_id
    }
    # 构建完整URL
    url = f"{url}?{urlencode(param)}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查HTTP错误

        # 解析JSON响应
        data = response.json()

        if data.get('result') == 1:
            active_list = data.get('data', {}).get('activeList', [])
            active_list.sort(key=lambda x: int(x['createtime']))
            return active_list
        else:
            print(f"API请求失败: {data.get('msg', '未知错误')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None


def extract_course_ids(html):
    """
    从HTML中提取课程实体并去重

    :param html: HTML内容
    :return: 包含唯一课程实体的集合
    """
    soup = BeautifulSoup(html, 'html.parser')
    courses = set()

    # 查找所有课程div
    course_divs = soup.find_all('div', class_='course')

    for div in course_divs:
        # 提取课程ID
        course_id = div.find('input', class_='courseId')['value']

        # 提取课程名称
        name_span = div.find('span', class_='course-name')
        course_name = name_span.get_text(strip=True) if name_span else "未知课程"

        # 创建实体并添加到集合
        courses.add(Course(course_id=course_id, course_name=course_name))
    return courses


def get_attendance_name(activity_id):
    url = 'https://mobilelearn.chaoxing.com/v2/apis/active/getPPTActiveInfo'
    param = {
        'activeId': activity_id
    }
    # 构建完整URL
    url = f"{url}?{urlencode(param)}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('result') == 1:
            return data.get('data', {}).get('name', '')
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None


def get_attendance_list(activity_id, class_id, course_id):
    url = 'https://mobilelearn.chaoxing.com/widget/sign/pcTeaSignController/getAttendList'
    param = {
        'fid': fid,
        'courseId': course_id,
        'classId': class_id,
        'activeId': activity_id
    }
    # 构建完整URL
    url = f"{url}?{urlencode(param)}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('result') == 1:
            # 创建临时字典存储本次考勤数据
            attendance_dict = {}
            # 处理已签到列表
            for student in data['data']['yiqianList']:
                name = student['name']
                status_key = str(student['status'])
                attendance_dict[name] = status_dict.get(status_key, status_key)
            # 处理未签到列表
            for student in data['data']['weiqianList']:
                name = student['name']
                status_key = str(student['status'])
                attendance_dict[name] = status_dict.get(status_key, status_key)
            return attendance_dict
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None


def write_attendance(activity_items, class_id, course_id, excel_path):
    count = 0
    for a in activity_items:
        if a.get('activeType') != 2 or a.get('createtime') <= time_limit:
            continue
        attendance_dict = get_attendance_list(activity_id=a['activeId'], class_id=class_id, course_id=course_id)
        if attendance_dict and len(attendance_dict) > 0:
            try:
                # 读取Excel文件
                df = pd.read_excel(excel_path, engine="openpyxl")
                col_name = a.get('title')
                # 添加新列到DataFrame
                # 将字典的键转换为 DataFrame
                if count == 0:
                    new_data = pd.DataFrame(list(attendance_dict.keys()), columns=['姓名'])
                    # 追加到原数据
                    df = pd.concat([df, new_data], ignore_index=True)
                    count = count + 1
                df[col_name] = df['姓名'].map(attendance_dict)
                df.to_excel(excel_path, index=False)
                print("done")
            except requests.exceptions.RequestException as e:
                print(f"请求发生错误: {e}")
                return None


courses = extract_course_ids(request_course_html())
for course_item in courses:
    if course_item.course_name not in course_list:
        continue
    script_path = Path(__file__).resolve()
    course_folder = script_path.parent / course_item.course_name
    # 创建文件夹
    course_folder.mkdir(exist_ok=True)
    class_json = class_by_course(course_item)
    for class_item in class_json:
        if class_item['name'] not in class_list:
            continue
        excel_path = script_path.parent / course_item.course_name / f"{class_item['name']}.xlsx"
        # 创建execl文件
        df = pd.DataFrame(columns=["姓名"])
        df.to_excel(excel_path, index=False, engine="openpyxl")
        activity_items = activity_course_class(course_id=course_item.course_id, class_id=class_item['id'])
        write_attendance(activity_items=activity_items, class_id=class_item['id'],
                         course_id=course_item.course_id, excel_path=excel_path)

# write_attendance(activity_id='6000121485923', class_id='114709224', course_id='249940325')
