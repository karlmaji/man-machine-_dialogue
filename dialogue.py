# -*- coding=utf-8 -*-
##百度问答API使用指南##
# #https://ai.baidu.com/ai-doc/UNIT/qkpzeloou
import requests
from urllib.parse import urlencode
from urllib.parse import quote_plus
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import URLError

API_KEY = 'tuXGzyBMMu0O0PSWzT4G395B'
API_SECRET='ueWt6T0XHZ8saSH4glFcwGtr6nTchG1j'
SERVICE_ID = 'S76849'

class UNIT:
    def __init__(self, api_key, api_secret,service_id):
        self.access_token = None
        self.url = None
        self.service_id = service_id
        self.set_access_token(api_key, api_secret)

    def set_access_token(self, api_key, api_secret):
        host = 'https://aip.baidubce.com/oauth/2.0/token?' \
               'grant_type=client_credentials&' \
               'client_id={0}&' \
               'client_secret={1}'.format(api_key, api_secret)
        response = requests.post(host)
        if response:
            self.access_token = response.json()['access_token']

    def query(self, query_text):
        self.url = 'https://aip.baidubce.com/rpc/2.0/unit/service/v3/chat?access_token=' + self.access_token
        post_data = "{\"version\":\"3.0\",\"service_id\":\"%s\",\
            \"session_id\":\"\",\"log_id\":\"20221027\",\
            \"request\":{\"terminal_id\":\"00000\",\"query\":\"%s\"}}" %(self.service_id,query_text)
        post_data = post_data.encode('utf-8')
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.url, data=post_data, headers=headers)
        if response:
            return response.json()['result']['responses'][0]['actions'][0]['say']

