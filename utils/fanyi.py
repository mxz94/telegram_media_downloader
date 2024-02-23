import os
import re
from time import sleep

import requests
import random
import json
from hashlib import md5
from xpinyin import Pinyin


# Set your own appid/appkey.
appid = '20180712000185166'
appkey = 'ShuYWsUO4MDfPswE8OWa'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'auto'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def translate(query, to_lang= "zh"):
    try:
        salt = random.randint(32768, 65536)
        sign = make_md5(appid + query + str(salt) + appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        rs = result.get("trans_result")
        if rs:
            return rs[0].get("dst")
    except Exception as e:
        return None

# 判断字符是否为汉字
def contains_chinese(input_str):
    for char in input_str:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

def find_text_in_quotes(file_path):
    content = None
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        s = content.__contains__("DictConfig")
        matches = re.findall(r'"([^"]*)"', content)
        # matches = re.findall(r'Result\.error\("([^"]+)"\)', content)
        # matches = re.findall(r'@NotBlank\(message\s*=\s*"([^"]+)"\)', content)

        if matches and s:
            for index, match in enumerate(matches, start=1):
                if contains_chinese(match):
                    sleep(2)
                    res = translate(match, "pt")
                    content = content.replace("\"%s\"" % match, "\"%s\"" % res)
                    print(f'Match {file_path}: {match} - {res}')
                    # print(f'Match {file_path}: {match}')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def read_all_file(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


# 用法示例
file_path = r'D:\mxz\custom-code-cabinet-api'  # 替换为实际文件路径
# find_text_in_quotes(file_path)
for e in read_all_file(file_path):
    if e.endswith("java"):
        find_text_in_quotes(e)

print(contains_chinese("232"))
print(translate("What Does a Typical Tibetan Farewell Party Look Like?"))