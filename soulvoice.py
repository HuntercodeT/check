import os

import requests
from bs4 import BeautifulSoup
import datetime, random, time

cookie = os.environ['soulvoice_cookie']

class soulvoice:
    def login(self,cookie):
        url = 'https://pt.soulvoice.club/attendance.php'

        headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        # time.sleep(random.randint(10, 1000)

        re = requests.get(url, headers=headers)
        content = re.text

        return content


    def check(self,content):

        soup = BeautifulSoup(content, features="html5lib")
        username = soup.select('span[class="nowrap"]>a>b')[0].get_text()
        tishi = soup.select('td[class="bottom"]')[0].get_text()
        total = tishi.split(':')[1].split(')')[0].split('(')[0]
        reward = tishi.split(':')[1].split(')')[0].split('(')[1]
        if '签到已得' in tishi and username == 'stones':
            code = 1
        else:
            code = 0
        return username,code,total,reward


    def pushplus(self, pushplus_token, content):
        url = 'http://www.pushplus.plus/send'
        html = content.replace("\n", "<br/>")
        data = {
            'token': pushplus_token,
            "title": "PTtime 签到通知",
            "content": html,
            'template': 'json'
        }
        requests.post(url=url, params=data)
    def main(self) :

        try:
            content = self.login(cookie)
            username, code, total, reward = self.check(content)
            if code == 1:
                message = username + '您好，聆音签到成功' + '\n' + '本次签到获得' + reward + ('魔力值') + '\n''当前总魔力值' + total
            else:
                message = '签到失败，请手动签到并检查'
        except:
            message = '签到失败，脚本出错'
        self.pushplus(os.environ['PUSHPLUS_TOKEN'], message)

if __name__ == '__main__':
    soulvoice().main()

