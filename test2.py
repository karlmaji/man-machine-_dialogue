# encoding:utf-8
import requests
API_KEY = 'tuXGzyBMMu0O0PSWzT4G395B'
API_SECRET='ueWt6T0XHZ8saSH4glFcwGtr6nTchG1j'
SERVICE_ID = 'S76849'
host = 'https://aip.baidubce.com/oauth/2.0/token?' \
        'grant_type=client_credentials&' \
        'client_id={0}&' \
        'client_secret={1}'.format(API_KEY, API_SECRET)
response = requests.post(host)
if response:
    access_token = response.json()['access_token']
    #access_token = '#####调用鉴权接口获取的token#####'
    url = 'https://aip.baidubce.com/rpc/2.0/unit/service/v3/chat?access_token=' + access_token
    post_data = "{\"version\":\"3.0\",\"service_id\":\"S76849\",\"session_id\":\"\",\"log_id\":\"7758521\",\"request\":{\"terminal_id\":\"88888\",\"query\":\"今天是礼拜几？\"}}"
    post_data = post_data.encode('utf-8')
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=post_data, headers=headers)
    if response:
        print (response.json())