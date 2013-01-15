#coding:utf8
import json
import urllib
import urllib2
import xml.etree.ElementTree as ET
import time
import random

__author__ = 'Sempr'

ads = [
    u'烦死啦！又有人在逼我乱发广告！就不发就不发，气死他！',
    u'那些个让我乱发广告的，诅咒他们吃方便面没有调料包！',
    u'我是头好驴，绝不发广告!',
    u'主淫主淫，他们不教我学好，只教我发广告！不好玩啊！',
]

def parse_txt(data):
    r = ET.fromstring(data)
    ret = dict()
    for x in r: ret[x.tag] = x.text
    return ret

def build_txt(values,text):
    r = ET.Element('xml')

    new_values = {}

    new_values['ToUserName'] = values['FromUserName']
    new_values['FromUserName'] = values['ToUserName']
    new_values['Content'] = text
    new_values['CreateTime'] = str(int(time.time()))
    new_values['MsgType'] = 'text'
    new_values['FuncFlag'] = '0'
    for k,v in new_values.items():
        x = ET.SubElement(r,k)
        x.text = v
    ret = ET.tostring(r,encoding='utf8')
    return ret


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
    ret = json.loads(data)
    if ret.get('result') == 100:
        res = ret['response']
        res = res.replace(u'鸡',u'驴')
        if res.find(u'微信')>=0: res=random.sample(ads,1)[0]
        return res
    else: return '休息啦！不要吵！烦死了!'

if __name__ == '__main__':
    values = dict(ToUserName='1',FromUserName='2')
    print build_txt(values,'hello!')

    cookie = get_cookie()
    print get_msg('小黄鸡!',cookie)


