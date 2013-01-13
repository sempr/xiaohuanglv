import xml.etree.ElementTree as ET
from hello.helpers import utils
import urllib

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
        if x.tag == 'Content': x.text = text.encode('utf8')
        if x.tag == 'ToUserName': from_u = x.text
        if x.tag == 'FromUserName': to_u = x.text
    for x in r:
        if x.tag == 'ToUserName': x.text = to_u
        if x.tag == 'FromUserName': x.text = from_u
    child = ET.Element('FuncFlag')
    child.text = '0'
    r.append(child)
    ret = ET.tostring(r)
    return ret

if __name__ == '__main__':
    data = """
<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 </xml>
    """
    text = parse_txt(data)
    r = build_txt(data,text)
    print r
