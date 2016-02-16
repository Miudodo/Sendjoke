#-*- coding:utf-8 -*-
__author__ = 'miudodo'


# -*- coding: utf-8 -*-
import sys, urllib, urllib2, json
import requests,re

def get_content():
    url = 'http://apis.baidu.com/showapi_open_bus/showapi_joke/joke_text?page=1'
    req = urllib2.Request(url)

    req.add_header("apikey", "4cdf54fb864a0fd7654a5c42aedd41ba")

    resp = urllib2.urlopen(req)
    content = resp.read()
    if(content):
        json_result = json.loads(content) #转换为字典对象
        #  下面从这个字典中获得笑话的标题和正文
        content_list = json_result['showapi_res_body']['contentlist']
        # 只取第一条笑话的标题和正文
        #first_title = content_list[0]['title'].encode('utf8')
        first_text = content_list[0]['text'].encode('utf8')
        #print '标题：'+first_title
        return '笑话：'+ first_text
    else:
        return "系统错误，无笑话"

def sendsms():
    url_1 = 'http://wapmail.10086.cn/loginie.htm?cmd=12&cv=2&swv=1'
    url_2 = 'https://wapmail.10086.cn/index.htm'

    #首页，获取JSESSIONID
    s = requests.session()
    cookie = s.get(url_1).cookies._cookies
    p = re.compile(r'JSESSIONID...value=.(.*?).,')
    jsessionid = p.findall(str(cookie))[0]
    Cookie = "%s=%s" % ("JSESSIONID",jsessionid)

    headers = {
        "Cookie":Cookie,
        "Host":"wapmail.10086.cn",
        "Origin":"http://wapmail.10086.cn",
        "Referer":url_1,
        "Upgrade-Insecure-Requests":1,
        "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
    }

    data = {
        "ur":"13928960513",
        "pw":"q387647979",
        "_fv":2,
        "submitInput":u"登录"
    }

    #登录邮箱，获取Cookie
    r = s.post(url_2, data = data, headers = headers, allow_redirects=False)
    p2 = re.compile(r'\'location\': \'(.*?)\'')
    p3 = re.compile(r'sid=(.*?)&')
    location =  p2.findall(str(r.headers))[0]
    sid = p3.findall(location)[0]
    cookies = str(r.cookies)
    #print location, sid
    p4 = re.compile(r'Cookie (.*?) for')
    cookies = p4.findall(str(cookies))
    for c in cookies:
        Cookie = Cookie + "; " + c
    #print Cookie


    #发送短信
    url_sms = 'http://wapmail.10086.cn/ws12/n2/send.htm?cmd=40&sid=%s' % sid
    url_send = 'http://wapmail.10086.cn/ws12/n2/send.htm'

    phone = '13928960513'

    headers["Referer"] = url_sms
    headers["Cookie"] = Cookie

    content = get_content()

    data_sms = {
        "sid":sid,
        "cmd":2,
        "rnum":012462,
        "l":1,
        "c":'',
        "s":'',
        "reciever":phone,
        "content": content,
        "signid":-1,
        "cmds":u"发送",
        "mailflag":1,
    }

    r_sms = s.post(url_send, data = data_sms, headers = headers)
    #print headers
    #print data_sms
    print r_sms.status_code

if __name__ == '__main__':
    sendsms()