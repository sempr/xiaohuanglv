# -*- encoding:utf-8 -*-
from flask import Module, request, render_template, current_app, Blueprint
from werkzeug.wsgi import LimitedStream

from xiaohuanglv.jobs.job0 import add
from xiaohuanglv.helpers import utils

frontend = Blueprint('',__name__)

@frontend.route('/test')
def test():
    return str(request.host)

@frontend.route('/add')
def index():
    a = request.values.get('a')
    b = request.values.get('b')
    if not a: a = 0
    if not b: b = 0
    a,b = int(a),int(b)
    for g in xrange(10):
        add.delay(g,a,b)
    return render_template('layout.html',msg='ok!')

@frontend.route('/weixin',methods=['GET'])
def weixin_get():
    echostr = request.values.get('echostr')
    if echostr: return echostr
    return weixin_post()

@frontend.route('/weixin',methods=['POST'])
def weixin_post():
    msg = get_input_data()
    if msg.get('MsgType') != 'text':
        return utils.build_txt(msg,'我只认识文字哒，图片地理位置以及表情神马的我都不认得哦~')

    cookie = current_app.config['cookie']
    ret = utils.get_msg(msg['Content'],cookie)
    print msg,ret
    try:
        new_ret = utils.build_txt(msg,ret)
    except:
        new_ret = ret
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

@frontend.route('/fanyi',methods=['POST','GET'])
def fanyi_post():
    msg = get_input_data()
    if msg.get('MsgType') != 'text': return utils.build_txt(msg,'我只认识文字哒，图片地理位置以及表情神马的我都不认得哦~')
    ret = utils.translate(msg['Content'])
    new_ret = utils.build_txt(msg,ret)
    return new_ret