# coding=utf-8
import json
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
from pathlib import Path
import pandas as pd

cookie = 'fid=11109; _uid=381235795; UID=381235795; xxtenc=4065a26bded7e381fe84dc6e3189ef57; source=""; thirdRegist=0; route=c010ccedb771f8b7c7793c67ee1d2aae; k8s=1744721000.468.17568.35332; spaceFid=11109; spaceRoleId=1; tl=1; orgfid=43843; registerCode=00010048000100010018; _d=1744723232719; vc3=RMkV1rM3qHFy9BP9tR7UI%2BmNjIpAFmk%2F4mCiJa2UqJQD5%2B8lcP4td%2FcjtV3DliovUmGdHkaPDyMvVHvIqovzQHNuK%2FE4QLGOlYLd%2BX%2Bj5eMXqHZ8PVyXVGqxx%2FlR5GVWL%2BPoVnnnXKibSeoZ42H%2FASInQEf3%2FtPTXtda6BSY5Bw%3D8755c545e6956455610c5af79f7d8029; uf=b2d2c93beefa90dc042df553c84db8fe3e00529daf8b4fd9ed898f55330f78561aa8965e419378ec660451fb5626896bd110c105546a283d26ce4e094e3f8fdfffcc3e0ecaa21d4f9e851954d33ea9726d0f06b5c9eac81ca5f2f33c8c1f840245bc2cc8f3dac912dfd4860a93fcbeea883843d4ba9fc84fe7c43f1a2f38e044577a9aa095a87b2c; cx_p_token=3b5f2b38e78b1cc31dad0f30af2f953b; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIzODEyMzU3OTUiLCJsb2dpblRpbWUiOjE3NDQ3MjMyMzI3MjAsImV4cCI6MTc0NTMyODAzMn0.nZjxFrJu_pi_rbU6mj6h316O97I9MNJRobiqPyYqhWA; DSSTASH_LOG=C_38-UN_10575-US_381235795-T_1744723232721; jrose=0790D64ED471CFAED12DE22FA6E55F5A.mooc2-2988524682-l6pwk'
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
               '5': '缺勤'}
course_list = ['']
class_list = ['']


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
            return data.get('data', {}).get('activeList', [])
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
    for course in courses:
        script_path = Path(__file__).resolve()
        course_folder = script_path.parent / course.course_name
        # 创建文件夹
        course_folder.mkdir(exist_ok=True)
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
                attendance_dict[name] = status_dict[status_key]
            # 处理未签到列表
            for student in data['data']['weiqianList']:
                name = student['name']
                status_key = str(student['status'])
                attendance_dict[name] = status_dict[status_key]
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
        if a.get('activeType') != 2:
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
    class_json = class_by_course(course_item)
    script_path = Path(__file__).resolve()
    for class_item in class_json:
        if class_item['name'] not in course_list:
            continue
        excel_path = script_path.parent / course_item.course_name / f"{class_item['name']}.xlsx"
        # 创建execl文件
        df = pd.DataFrame(columns=["姓名"])
        df.to_excel(excel_path, index=False, engine="openpyxl")
        activity_items = activity_course_class(course_id=course_item.course_id, class_id=class_item['id'])
        write_attendance(activity_items=activity_items, class_id=class_item['id'],
                         course_id=course_item.course_id, excel_path=excel_path)

# write_attendance(activity_id='6000121485923', class_id='114709224', course_id='249940325')
