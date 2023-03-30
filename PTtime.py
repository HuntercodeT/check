import os
import logging
import requests
from bs4 import BeautifulSoup
import datetime, random, time

cookie = os.environ['pttime_cookie']

class PTtime:
    def login(self,cookie):
        url = 'https://www.pttime.org/attendance.php'

        headers = {
            'cookie': cookie,
            'referer': 'https://www.pttime.org/attendance.php',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        time.sleep(random.randint(10, 1000))
        re = requests.get(url, headers=headers)
        content = re.text

        return content


    def check(self,content):
        soup = BeautifulSoup(content, features="html5lib")
        username = soup.select('b')[0].get_text()
        selftime = soup.select('span[class="dib w200 pr20"]')[0].get_text().split('：')[1].split(' ')[0]
        value = soup.select('span[class="dib w150"]')[0].get_text()
        time_t = soup.select('span[class="dib w200 pr20"]')[0].get_text()
        selftoday = datetime.date.today()
        logging.info(f'{username} {tishi}')
        # print(time_1)
        if str(selftoday) == selftime:
            code = 1
        else:
            code = 0
        return code, value, time_t

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

    def main(self):
        try:
            content = self.login(cookie)
            code, value, time_t = self.check(content)
            if code == 1:
                message = "您好，PTtime签到成功\n" + '获得魔力值：' + str(value) + '\n实际签到' + str(time_t)
            else:
                message = '签到失败，请手动签到并检查'
        except:
            message = '签到失败，脚本出错'
        self.pushplus(os.environ['PUSH_PLUS_TOKEN'], message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    PTtime().main()

