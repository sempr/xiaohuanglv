import xml.etree.ElementTree as ET
from hello.helpers import utils

__author__ = 'Sempr'

def parse_txt(data):
    r = ET.fromstring(data)
    for x in r:
        if x.tag == 'Content': return x.text
    return ''

def build_txt(data,text):
    r = ET.fromstring(data)
    for x in r:
        if x.tag == 'Content': x.text = text
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
