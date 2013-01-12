#coding:utf8
import json
import urllib

__author__ = 'Sempr'

import urllib2

def get_cookie():
    url = 'http://www.simsimi.com/talk.htm'
    r = urllib2.urlopen(url)
    cookie = r.headers['Set-Cookie'].split(';')[0]
    return cookie

def get_msg(msg,cookie):
    data = urllib.urlencode({'msg':msg,'lc':'ch'})
    url = "http://www.simsimi.com/func/req?" + data
    req = urllib2.Request(url)
    req.add_header('Referer','http://www.simsimi.com/talk.htm')
    req.add_header('Cookie',cookie)
    r = urllib2.urlopen(req)
    data = r.read()
    print data
    ret = json.loads(data)
    if ret.get('result') == 100:
        res = ret['response']
        res = res.replace(u'鸡',u'驴')
        return res
    else: return '休息啦！不要吵!烦死了!'

if __name__ == '__main__':
    cookie = get_cookie()
    print get_msg('小黄鸡!',cookie)


