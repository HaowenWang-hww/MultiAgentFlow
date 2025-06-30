import os
import requests
import json
import openpyxl
import unicodedata
from openpyxl import Workbook
from pprint import pprint

directory = r'/Users/jnchou/Downloads/产品测试图'
prompt = '以上内容是通过图片识别得出的食物清单，请根据该清单计算能量、碳水化合物、微量元素、维生素等含量并给出分析与建议'
access_token = 'app-0jzvDbNexeaXotspQrE8vJuw'
wb = Workbook()
ws = wb.active

ws.append(['文件名','识别名','分析结果'])
for path, folders, files in os.walk(directory):
    for f in files:
        if '.py' not in f and '.xlsx' not in f:
            f_name = directory + '/' + f
            print(f_name)
            file_bytes = open(f_name,"rb").read()
            r = requests.post("http://10.30.10.232:5004/inference",files={"file":file_bytes})
            r_json = r.json()
            r_res = r_json['results']
            print(r_res)
            for result in r_res:
                o_name = result['label']
                r2_dict = {
                    "inputs": {},
                    "query": json.dumps(o_name, ensure_ascii=False) + prompt,
                    "response_mode": "blocking",
                    "conversation_id": "",
                    "user": "script",
                    "files": []
                }
                r2_headers = {
                    "Authorization": 'Bearer ' + access_token,
                    'Content-Type': 'application/json'
                }
                r2 = requests.post("http://10.30.10.105:8502/v1/chat-messages", json=r2_dict, headers=r2_headers)
                # print(r2.text)
                try:
                    o_summary = r2.json()['answer']
                except Exception as e:
                    o_summary = ""
                ws.append([f,
                           o_name,
                           o_summary])
    wb.save('out.xlsx')
