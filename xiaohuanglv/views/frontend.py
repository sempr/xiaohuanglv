# -*- encoding:utf-8 -*-
from flask import Module, request, render_template, current_app, Blueprint
from werkzeug.wsgi import LimitedStream

from xiaohuanglv.helpers import utils

frontend = Blueprint('',__name__)

@frontend.route('/test')
def test():
    return str(request.host)

@frontend.route('/weixin',methods=['GET'])
@frontend.route('/fanyi',methods=['GET'])
def weixin_get():
    echostr = request.values.get('echostr')
    if echostr: return echostr
    return weixin_post()

@frontend.route('/weixin',methods=['POST'])
def weixin_post():
    msg = get_input_data()
    if msg.get('MsgType') != 'text': return utils.build_txt(msg,'我只认识文字哒，图片地理位置以及表情神马的我都不认得哦~')
    cookie = current_app.config['cookie']
    if msg['Content'] == 'Hello2BizUser': ret = '你好，欢迎关注小黄驴，我可以陪你聊天哒~'
    else: ret = utils.get_msg(msg['Content'],cookie)
    new_ret = utils.build_txt(msg,ret)
    return new_ret

def get_input_data():
    content_length = request.headers.get('content-length', type=int)
    if content_length > 0:
        stream = LimitedStream(request.environ['wsgi.input'], content_length)
        old_msg = stream.read()
        msg = utils.parse_txt(old_msg)
    else:
        text = request.values.get('text','')
        msg = {'Content':text, 'MsgType':'text'}
    return msg

@frontend.route('/fanyi',methods=['POST'])
def fanyi_post():
    msg = get_input_data()
    if msg.get('MsgType') != 'text': return utils.build_txt(msg,'我只认识文字哒，图片地理位置以及表情神马的我都不认得哦~')
    if msg['Content'] == 'Hello2BizUser': ret = '你好，欢迎关注翻译帝，我可以帮您做些简单的中英文互译的工作\n您可以尝试发给我"你好!"试一下哦!'
    else: ret = utils.translate(msg['Content'])
    new_ret = utils.build_txt(msg,ret)
    return new_ret
