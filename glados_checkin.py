import requests
import os

cookies = os.environ['GLADOS_COOKIES']
class Glados:
    def login(self, cookies):
        headers = {
            'authority': 'glados.rocks',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'authorization': '1107979040659170353175691805430-864-1536',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookies,
            'dnt': '1',
            'origin': 'https://glados.rocks',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }

        json_data = {
            'token': 'glados.network',
        }

        response = requests.post('https://glados.rocks/api/user/checkin',  headers=headers, json=json_data)

        try:
            msg = response.json()['message']
        except:
            msg = '签到失败，请手动签到并检查'
        return msg

    def reopen(self,cookies):

        headers = {
            'authority': 'glados.one',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'authorization': '7916806822158174279434491371426-1440-2560',
            'cache-control': 'no-cache',
            'cookie': cookies,
            'dnt': '1',
            'origin': 'https://glados.one',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        requests.post('https://glados.one/api/user/reopen', headers=headers)


    def pushplus(self, pushplus_token, content):
        url = 'http://www.pushplus.plus/send'
        html = content.replace("\n", "<br/>")
        data = {
            'token': pushplus_token,
            "title": "glados 签到通知",
            "content": html,
            'template': 'html'
        }
        requests.post(url=url, params=data)
    def main(self):
        cookies_list = cookies.split('&')
        for cookie in cookies_list:
            msg = self.login(cookie)
            print(msg)
            self.reopen(cookie)
            self.pushplus(os.environ['PUSH_PLUS_TOKEN'], msg)

if __name__ == '__main__':
    Glados().main()