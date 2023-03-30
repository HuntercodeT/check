import os
import requests
from bs4 import BeautifulSoup
import logging

cookie = os.environ['ptschool_cookies']

class PTSchool:
    def login(self,cookie):
        headers = {
            'authority': 'pt.btschool.club',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            # Requests sorts cookies= alphabetically
            'cookie':cookie,
            'dnt': '1',
            'pragma': 'no-cache',
            'referer': 'https://pt.btschool.club/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

        params = {
            'action': 'addbonus',
        }

        response = requests.get('https://pt.btschool.club/index.php', params=params, headers=headers)
        # 检测响应内容的编码格式
        # encoding = response.encoding
        # logging.info(encoding)
        # if encoding is None:
        #     encoding = chardet.detect(response.content)['encoding']
        #
        # # 保存响应内容到本地HTML文件中，指定编码格式为gb2312
        # with open('ptschool.html', 'w', encoding=encoding) as html_file:
        #     html_file.write(response.text)
        # # content = response.content.decode('utf-8')
        soup = BeautifulSoup(response.text, features="html5lib")
        user = soup.select('#info_block > tbody > tr > td > table > tbody > tr > td:nth-child(1) > span > span > a > b')[0].get_text()
        value = soup.select('#outer > p > table > tbody > tr > td > b > a > font')[0].get_text()
        msg = f'{user} 签到成功，{value}'
        logging.info(msg)
        return msg

    def pushplus(self, pushplus_token, content):
        url = 'http://www.pushplus.plus/send'
        html = content.replace("\n", "<br/>")
        data = {
            'token': pushplus_token,
            "title": "ptschool 签到通知",
            "content": html,
            'template': 'txt'
        }
        requests.post(url=url, params=data)

    def main(self):
        msg = self.login(cookie)
        logging.info(msg)
        self.pushplus(os.environ['PUSH_PLUS_TOKEN'], msg)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    PTSchool().main()
