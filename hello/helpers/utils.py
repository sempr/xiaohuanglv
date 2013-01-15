#coding:utf8
import json
import urllib
import urllib2
import xml.etree.ElementTree as ET

__author__ = 'Sempr'

def parse_txt(data):
    r = ET.fromstring(data)
    for x in r:
        if x.tag == 'Content': return x.text
    return ''

def build_txt(data,text):
    r = ET.fromstring(data)
    from_u = to_u = ''
    for x in r:
        if x.tag == 'Content': x.text = text
        if x.tag == 'ToUserName': from_u = x.text
        if x.tag == 'FromUserName': to_u = x.text
    for x in r:
        if x.tag == 'ToUserName': x.text = to_u
        if x.tag == 'FromUserName': x.text = from_u
    child = ET.Element('FuncFlag')
    child.text = '0'
    r.append(child)
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
        if res.find(u'微信')>=0: res=u'烦死啦！又有人在逼我乱发广告！就不发就不发，气死他！'
        return res
    else: return '休息啦！不要吵！烦死了!'

if __name__ == '__main__':
    cookie = get_cookie()
    print get_msg('小黄鸡!',cookie)


