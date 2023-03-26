#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author: Bean
# datetime:2022/11/27 19:01
# -*- coding: utf-8 -*-
import urllib3
urllib3.disable_warnings()
import json
import requests
import os

#账户
EMAIL = os.environ['ikuuu_email']
PASSWORD = os.environ['ikuuu_password']
DOMAIN = 'https://ikuuu.eu'
# pushplus 推送
PushPlus_Token = os.environ['PUSH_PLUS_TOKEN']

# 企业微信配置
QYWX_CORPID = 'wwfe51xxx'
QYWX_AGENTID = '1000xx'
QYWX_CORPSECRET = '6KyJTxxxx'
QYWX_TOUSER = 'ikuuu签到'
QYWX_MEDIA_ID = '2COo-kxxxx'

class SSPANEL:
    name = "SSPANEL"

    def __init__(self, check_item):
        self.check_item = check_item
        self.qywx_corpid = QYWX_CORPID
        self.qywx_agentid = QYWX_AGENTID
        self.qywx_corpsecret = QYWX_CORPSECRET
        self.qywx_touser = QYWX_TOUSER
        self.qywx_media_id = QYWX_MEDIA_ID
        self.pushplus_token = PushPlus_Token

    def pushplus(self,pushplus_token,content):
        url = 'http://www.pushplus.plus/send'
        html = content.replace("\n", "<br/>")
        data = {
            'token': pushplus_token,
            "title": "ikuuu 签到通知",
            "content": html,
            'template': 'json'
        }
        requests.post(url=url, params=data)
    def message2qywxapp(self, qywx_corpid, qywx_agentid, qywx_corpsecret, qywx_touser, qywx_media_id, content):
        print("企业微信应用消息推送开始")
        res = requests.get(
            f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={qywx_corpid}&corpsecret={qywx_corpsecret}"
        )
        token = res.json().get("access_token", False)
        if qywx_media_id:
            data = {
                "touser": qywx_touser,
                "msgtype": "mpnews",
                "agentid": int(qywx_agentid),
                "mpnews": {
                    "articles": [
                        {
                            "title": "ikuuu 签到通知",
                            "thumb_media_id": qywx_media_id,
                            "content_source_url": "https://ikuuu.co/",
                            "content": content.replace("\n", "<br>"),
                            "digest": content,
                        }
                    ]
                },
            }
        else:
            data = {
                "touser": qywx_touser,
                "agentid": int(qywx_agentid),
                "msgtype": "textcard",
                "textcard": {
                    "title": "ikuuu 签到通知",
                    "description": content,
                    "url": "https://ikuuu.co/",
                },
            }
        result = requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}",
                               data=json.dumps(data))
        print(result)
        return

    # 企业微信通知，普通微信可接收
    def sendWechat(self,wex_id, wex_secret, wx_agentld, content, thumb_media_id='', title='', author=''):
        try:
            # 获得access_token
            url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
            token_param = '?corpid=' + wex_id + '&corpsecret=' + wex_secret
            token_data = requests.get(url + token_param)
            token_data.encoding = 'utf-8'
            token_data = token_data.json()
            access_token = token_data['access_token']
            # 发送内容
            html = content.replace("\n", "<br/>")
            if thumb_media_id:
                data = {
                    "touser": "@all",
                    "msgtype": "mpnews",
                    "agentid": wx_agentld,
                    "mpnews": {
                        "articles": [
                            {
                                "title": title,
                                "thumb_media_id": thumb_media_id,
                                "author": author,
                                "content_source_url": "",
                                "content": html,
                                "digest": content
                            }
                        ]
                    }
                }
            else:
                data = {
                    "touser": "@all",
                    "msgtype": "text",
                    "agentid": wx_agentld,
                    "text": {"content": content}
                }
            send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
            message = requests.post(send_url, json=data)
            message.encoding = 'utf-8'
            res = message.json()
            print('Wechat send : ' + res['errmsg'])
        except Exception as e:
            print('微信通知推送异常，原因为: ' + str(e))
    def sign(self, email, password, url):
        email = email.replace("@", "%40")
        try:
            session = requests.session()
            session.get(url=url, verify=False)
            login_url = url + "/auth/login"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
            post_data = "email=" + email + "&passwd=" + password + "&code="
            post_data = post_data.encode()
            session.post(login_url, post_data, headers=headers, verify=False)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Referer": url + "/user",
            }
            response = session.post(url + "/user/checkin", headers=headers, verify=False)
            msg = response.json().get("msg")
        except Exception as e:
            msg = "签到失败"
        print(msg)
        return msg

    def main(self):
        email = self.check_item.get("email")
        password = self.check_item.get("password")
        url = self.check_item.get("url")
        qywx_corpid = self.qywx_corpid
        qywx_agentid = self.qywx_agentid
        qywx_corpsecret = self.qywx_corpsecret
        qywx_touser = self.qywx_touser
        qywx_media_id = self.qywx_media_id
        pushplus_token = self.pushplus_token
        sign_msg = self.sign(email=email, password=password, url=url)
        msg = [
            {"name": "帐号信息", "value": email},
            {"name": "签到信息", "value": f"{sign_msg}"},
        ]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        # self.message2qywxapp(qywx_corpid=qywx_corpid, qywx_agentid=qywx_agentid, qywx_corpsecret=qywx_corpsecret,
        #                      qywx_touser=qywx_touser, qywx_media_id=qywx_media_id, content=msg)
        if self.pushplus_token:
            self.pushplus(pushplus_token,msg)
        else:
            self.sendWechat(qywx_corpid, qywx_corpsecret,qywx_agentid, msg,qywx_media_id,"ikuuu_sign","Bean")
        return msg



if __name__ == "__main__":
    _check_item = {'email': EMAIL, 'password': PASSWORD, 'url': DOMAIN}
    SSPANEL(check_item=_check_item).main()