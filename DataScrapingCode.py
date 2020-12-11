#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import csv
from harvesttext import HarvestText
import json
import os
from requests.packages import urllib3

SAVE_FILE = "./comments_413_last.csv"
#  SAVE_FILE = "./comments_917.csv"
if os.path.exists(SAVE_FILE):
    os.remove(SAVE_FILE)
with open(SAVE_FILE, 'w') as f:
    f.write("name,user_gender,user_id,comment_time,comment_info\n")

# 以下的ID是413
ID_MID = 4493278155789274
# 以下的ID是917
#  ID_MID = 4550160384268249

session = requests.session()


class WeiboContent:
    def __init__(self):
        self.start_url = f'https://m.weibo.cn/comments/hotflow?id={ID_MID}&mid={ID_MID}'
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "cookie": "WEIBOCN_FROM=1110006030; loginScene=102003; SUB=_2A25yuApWDeRhGeFL6VQS9C_KzjiIHXVuQpYerDV6PUJbkdANLWamkW1NQlcdgiMi03bezcdlD4mSyWWUuAQHgC4X; MLOGIN=1; _T_WM=33441482076; XSRF-TOKEN=ba2431; M_WEIBOCN_PARAMS=oid%3D4493278155789274%26luicode%3D20000061%26lfid%3D4493278155789274%26uicode%3D20000061%26fid%3D4493278155789274",
            #  "cookie": "WEIBOCN_FROM=1110006030; loginScene=102003; SUB=_2A25yuOLDDeRhGedG7VES8yzIyDmIHXVuQo6LrDV6PUJbkdANLU78kW1NUQuLzCq50MfSj8MwwuCgitQc-IDQLQ0_; _T_WM=98497638108; XSRF-TOKEN=efecfe; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4550160384268249%26luicode%3D20000061%26lfid%3D4550160384268249%26uicode%3D20000061%26fid%3D4550160384268249",
            "pragma": "no-cache",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "same-origin",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }

    def write_csv(self, data, data_path):
        headers = ['name', 'user_gender', 'user_id', 'comment_time', 'comment_info']
        with open(data_path, 'a', encoding='utf-8') as f:
            csv_write = csv.DictWriter(f, headers)
            csv_write.writerows(data)

    def getHTMLTest(self, url):
        try:
            urllib3.disable_warnings()
            r = session.get(url=url, headers=self.headers, verify=False)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print(r.status_code)
            if not r.json()['ok']:
                print(r.text)
                raise Exception
            return r.text
        except Exception as e:
            print('请求页面失败...', e)
            return ""

    def getList(self, html):
        ht = HarvestText()
        total_comments = []
        resjson = json.loads(html)
        Data = resjson.get('data')
        max_id = Data.get('max_id')
        max_id_type = Data.get('max_id_type')
        total_number = Data.get('total_number')
        data = Data.get('data')
        for i in range(len(data)):
            try:
                ttime = data[i].get('created_at')
                user = data[i].get('user')
                user_name = user.get('screen_name')
                gender = user.get('gender')
                user_id = user.get('id')
                #  user_info_url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={user_id}&containerid=230283{user_id}'
                #  html = self.getHTMLTest(user_info_url)
                #  if html != "":
                    #  res_json = json.loads(html)['data']['cards'][1]
                    #  if res_json['card_group'] == [] or 'item_content' not in res_json['card_group'][1]:
                        #  user_age = '无'
                        #  user_livingplace = '无'
                    #  else:
                        #  user_info = res_json['card_group'][1]['item_content']
                        #  if '岁' in user_info and '座' in user_info:
                            #  user_info = re.search(r'.* (\d+)岁.*座  (.*)', user_info)
                            #  user_age = user_info.group(1)
                            #  user_livingplace = user_info.group(2)
                        #  elif '座' in user_info:
                            #  user_info = re.search(r'.*座  (.*)', user_info)
                            #  user_age = '无'
                            #  user_livingplace = user_info.group(1)
                        #  else:
                            #  user_info = re.search(r'.*  (.*)', user_info)
                            #  user_age = '无'
                            #  user_livingplace = user_info.group(1)
                #  else:
                    #  user_age = '无'
                    #  user_livingplace = '无'

                text = ht.clean_text(data[i].get('text'))  # 清理文本，将一些<span>或表情包删掉仅保留文字
                item = {}
                item["name"] = user_name  # 存储评论人的网名
                item["user_gender"] = gender  # 存储评论人的相关性别
                item["user_id"] = user_id  # 存储评论人的相关主页
                item["comment_time"] = ttime  # 存储评论时间
                item["comment_info"] = text  # 存储评论的信息
                total_comments.append(item)

            except Exception as e:
                print('出现了异常哦：', e)
        print('抓取到了{}/{}条评论，以下是其中的一条\n{}'.format(len(total_comments), len(data), total_comments[0]))
        return total_comments, max_id, max_id_type, total_number

    def run(self):
        times = 0  # 方便查看请求了数据接口多少次
        current_nums, total_nums = 0, 0
        max_id, max_id_type = None, 0
        while True:
            # 用三元表达式来生成请求的URL
            comment_url = self.start_url + '&max_id={}&max_id_type={}'.format(max_id, max_id_type) if max_id else self.start_url + '&max_id_type=0'
            print('[{}]-'.format(times) + comment_url + '...', end='')
            times += 1
            # 发送请求，并得到数据接口返回的内容
            html = self.getHTMLTest(comment_url)
            time.sleep(1)
            # 如果得不到内容则跳过此循环，中止程序。
            if not html:
                print('无法请求当前页面的数据接口...需重新启动程序')
                break
            # 将数据接口所给的内容，放进json中并提取所需的数据
            data, max_id, max_id_type, total_nums = self.getList(html)
            current_nums += len(data)
            print('目前已抓取{}/{}\n-----------------------------------------------------'.format(current_nums, total_nums))
            # 保存到csv文件中！
            self.write_csv(data, SAVE_FILE)
            if not max_id:
                print('已经没有数据可拿了...{}-{}'.format(max_id_type, max_id))
                break


if __name__ == '__main__':
    weibo = WeiboContent()
    weibo.run()
