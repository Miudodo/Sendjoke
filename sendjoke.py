#-*- coding:utf-8 -*-
__author__ = 'miudodo'

import requests,re

def get_content():
    url = 'http://apis.baidu.com/showapi_open_bus/showapi_joke/joke_text?page=1'

    headers = {
        "apikey":"4cdf54fb864a0fd7654a5c42aedd41ba"
    }

    content = requests.get(url, headers = headers)
    if(content):
        result = ''.join(content.text) #转换文本
        # 使用正则获取笑话正文
        p_joke = re.compile(r'"text":"(.*?)"')
        text = p_joke.findall(result)
        # 只取第一条笑话正文
        #for t in text:
        #    print t
        return u'笑话：'+ text[0]
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
        "ur":"***********",  #139邮箱账号
        "pw":"********",  #139邮箱密码
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

    phone = '********' #接收短信的号码

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
