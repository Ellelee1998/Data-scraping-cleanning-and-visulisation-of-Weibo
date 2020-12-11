{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 113,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "import csv\n",
    "import time\n",
    "import json\n",
    "import re\n",
    "\n",
    "user_ids = []\n",
    "with open('comments_413_final.csv', 'r', encoding='utf8')as f:\n",
    "    f_csv = csv.reader(f)\n",
    "    for row in f_csv:\n",
    "        user_ids.append(row[2])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 114,
   "metadata": {},
   "outputs": [],
   "source": [
    "save_csv_headers = ['user_id','user_age','user_livingplace']\n",
    "save_file = 'comments_413_more.csv'\n",
    "total_userinfo = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 115,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2381150031-24-四川 绵阳\n",
      "2381150031-24-四川 绵阳\n",
      "6376769819-22-重庆\n",
      "7264580536-23-四川\n",
      "3531189190-无-无\n",
      "2614152813-无-无\n"
     ]
    }
   ],
   "source": [
    "# 抓取第10-15个，例子\n",
    "for user_id in user_ids[10:16]:\n",
    "    user_mainpage_url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={user_id}&containerid=230283{user_id}'\n",
    "    headers = {\n",
    "        \"accept\": \"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\",\n",
    "        \"accept-encoding\": \"gzip, deflate, br\",\n",
    "        \"accept-language\": \"zh-CN,zh;q=0.9\",\n",
    "        \"cookie\": \"WEIBOCN_FROM=1110006030; loginScene=102003; SUB=_2A25y1kuNDeRhGeFL6VQS9C_KzjiIHXVuOVXFrDV6PUJbkdANLVCtkW1NQlcdgoIs6uP4ly2CYmYnvwN2zLunWP-U; _T_WM=34016050747; XSRF-TOKEN=587d11; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4493278155789274%26luicode%3D10000011%26lfid%3D1005052212037882%26fid%3D1076032212037882%26uicode%3D10000011\",\n",
    "        \"cache-control\": \"no-cache\",\n",
    "        \"pragma\": \"no-cache\",\n",
    "        \"sec-fetch-dest\": \"empty\",\n",
    "        \"sec-fetch-mode\": \"same-origin\",\n",
    "        \"sec-fetch-site\": \"same-origin\",\n",
    "        \"upgrade-insecure-requests\": \"1\",\n",
    "        \"user-agent\": \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36\"\n",
    "    }\n",
    "\n",
    "    try:\n",
    "        response = requests.get(url=user_mainpage_url, headers=headers)\n",
    "        if response.status_code == 200:\n",
    "            response_json = json.loads(response.text)\n",
    "        else:\n",
    "            print(response.text)\n",
    "    except Exception as e:\n",
    "        print(f'Error:{response.status_code}---{e}---')\n",
    "    if response_json['ok']:\n",
    "        data = response_json['data']\n",
    "        if len(data['cards'][1]['card_group']) != 0 and 'item_content' in data['cards'][1]['card_group'][1]:\n",
    "            user_info = data['cards'][1]['card_group'][1]['item_content']\n",
    "            if re.search(r'.*(\\d.+)岁.*座  (\\w.+)', user_info):\n",
    "                ans = re.search(r'.*(\\d.+)岁.*座  (\\w.+)', user_info)\n",
    "                user_age = ans.group(1)\n",
    "                user_livingplace = ans.group(2)\n",
    "                print(user_id + f'-{user_age}-{user_livingplace}')\n",
    "                total_userinfo.append([user_id, user_age, user_livingplace])\n",
    "            elif re.search(r'.*座  (\\w.+)', user_info):\n",
    "                user_livingplace = ans.group(1)\n",
    "                total_userinfo.append([user_id, '无', user_livingplace])\n",
    "                print(user_id + f'-无-{user_livingplace}')\n",
    "            elif re.search(r'.*(\\d.+)岁  (\\w.+)', user_info):\n",
    "                user_age = ans.group(1)\n",
    "                total_userinfo.append([user_id, user_age, '无'])\n",
    "                print(user_id + f'-{user_age}-无')\n",
    "            else:\n",
    "                total_userinfo.append([user_id, '无', '其他'])\n",
    "                print(user_id + '-无-其他')\n",
    "        else:\n",
    "            print(user_id + '-无-无')\n",
    "            total_userinfo.append([user_id, '无', '无'])\n",
    "    time.sleep(2.5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 116,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open(save_file,'w', encoding='utf8')as f:\n",
    "    f_csv = csv.writer(f)\n",
    "    f_csv.writerow(save_csv_headers)\n",
    "    f_csv.writerows(total_userinfo)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
