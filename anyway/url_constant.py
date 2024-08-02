import enum


class MyURL(enum.Enum):
    CREATE_TASK = {
                      'url': '/dream/app/api/task-center/create-or-update-task',
                      'data': {
                          "taskName": "来来来",
                          "taskStartTime": "1693989909331",
                          "taskEndTime": "1693993509331",
                          "personInChargeList": [
                              {
                                  "key": "212806",
                                  "label": "mysteel",
                                  "departmentName": "技术中心"
                              }
                          ],
                          "accepterInfo": {
                              "key": "218901",
                              "label": "李永辉",
                              "departmentName": "技术中心"
                          },
                          "estimatedWork": "222",
                          "priority": "2",
                          "importance": "2",
                          "focusPersonList": [],
                          "progress": "",
                          "synSchedule": "0",
                          "detail": "",
                          "attachedFile": [],
                          "subtaskIds": [],
                          "parentId": ""
                      },
                      'param': {"protocolVersion": "1.0.0"},
                      'method': 'POST'
                  },
    TASK_DETAIL = {
                      'url': '/dream/app/api/task-center/detail',
                      'param': {"queryType": 1,
                                "taskId": 6746710,
                                "protocolVersion": "1.0.0"},
                      'method': 'GET'
                  },
    PARENT_TASKS = {
        'url': '/dream/app/api/task-center/parent-task',
        'param': {
            'pageIndex': 1,
            'pageSize': 20,
            'excludeId': 7833866,
            'protocolVersion': '0.0.0'
        },
        'method': 'GET'
    }
