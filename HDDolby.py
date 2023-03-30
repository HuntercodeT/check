import os
import logging
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
        soup = BeautifulSoup(re.text, features="html5lib")
        msg = soup.select('span[class="medium"]')[0].get_text().split('(')[2].split(')')[0]
        logging.info(f'{msg}')
        return msg

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
                msg = self.login(cookie)
            except:
                msg = '签到失败，脚本出错'
            print(msg)
            self.pushplus(os.environ['PUSH_PLUS_TOKEN'], msg)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    HDDolby().main()

