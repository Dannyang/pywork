# coding=utf-8
import json
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
from pathlib import Path
import pandas as pd

cookie = 'fid=167983; _uid=159598606; _d=1744866937210; UID=159598606; vc3=EXYt6xjUl0hcVtHTyYW4kPMHytqvyeFV0Q8N3M%2FO7sfXBP8BN3lh%2Fz4jTGaAuu9J8X19IEn26FRi%2BFMcFwRD43yaPBElBaAeZP%2F17OixwAF3VqR1xdftO81zl5pdPm1KX2KKDd7JMPDFVVCa0o4DDA2Joar28p9YaoAcnLOFhYM%3D91641d6fb8700f2f0711b98885793d8e; uf=b2d2c93beefa90dc0e58f5e20478320846deb320366635b8ccd272461f400c99500856e34427f8f6cfec2656b3752fc66e05ed12397b5ca065057927e8f99f961a9cfffaba7b49c29c456714c93a27acb11b62c52d1197adc4a35a8edc5ea02f37df08321706ec2470184964ffe8c27c66e2c6168d73cb305a01432e9a5fb18db1f899d50c1c3fa3aa2ebad65cd196bb; cx_p_token=09b77a35ff6b3d9b04f8e2c0932354c1; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIxNTk1OTg2MDYiLCJsb2dpblRpbWUiOjE3NDQ4NjY5MzcyMTIsImV4cCI6MTc0NTQ3MTczN30.V7PXCUXSRqU7pONvujepaLSqJCF3rMw_qG8f2PuHLIs; xxtenc=fba95c7cadc0ec909232a3f602a34229; DSSTASH_LOG=C_38-UN_10575-US_159598606-T_1744866937212; source=""; thirdRegist=0; tl=1; route=44030bc8a3c0af15b8ff79c9243587ed; JSESSIONID=1933E80242F17D78D0D3FF06F3E7A776; route_mobilelearn=55d5bc3aa72a09ebb5e840d12718eff4; route_widget=fa72976f7522b88e057f37f2542fb7e4'
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
    script_path = Path(__file__).resolve()
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
