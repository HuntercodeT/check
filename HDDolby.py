import os

import requests
from bs4 import BeautifulSoup
import datetime, random, time

cookie = os.environ['hddolby_cookie']
class HDDolby:
    def login(self,cookie):
        url = 'https://www.hddolby.com/attendance.php'

        headers = {
            'cookie': cookie,
            'referer': 'https://www.hddolby.com/torrents.php',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        time.sleep(random.randint(10, 500))
        re = requests.get(url, headers=headers)
        content = re.text
        return content


    def check(self,content):
        soup = BeautifulSoup(content, features="html5lib")
        username = soup.select('b')[0].get_text()
        tishi = soup.select('span[class="medium"]')[0].get_text().split('(')[2].split(')')[0]
        if '签到已得' in tishi and username == 'stones':
            code = 1
        else:
            code = 0
        return username, tishi,code


    def pushplus(self, pushplus_token, content):
        url = 'http://www.pushplus.plus/send'
        html = content.replace("\n", "<br/>")
        data = {
            'token': pushplus_token,
            "title": "HDdolby 签到通知",
            "content": html,
            'template': 'json'
        }
        requests.post(url=url, params=data)
    def main(self) :
            try:
                content = self.login(cookie)
                username, tishi, code = self.check(content)
                if code == 1:
                    message = username + '您好，HDDolby签到成功' + '\n' + '本次签到获得' + tishi + ('魔力值')
                else:
                    message = '签到失败，请手动签到并检查'
            except:
                message = '签到失败，脚本出错'
            print(message)
            self.pushplus(os.environ['PUSH_PLUS_TOKEN'], message)

if __name__ == '__main__':
    HDDolby().main()

