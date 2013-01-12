# -*- encoding:utf-8 -*-
from flask import Module, request, render_template, current_app

from hello.jobs.job0 import add
from hello.helpers import utils,parser

frontend = Module(__name__)

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
    echostr = request.values.get('echostr')
    if echostr: return echostr
    old_msg = request.values.get('msg','hi')
    try:
        msg = parser.parse_txt(old_msg)
    except:
        msg = old_msg
    cookie = current_app.config['cookie']
    ret = utils.get_msg(msg,cookie)
    try:
        new_ret = parser.build_txt(old_msg,ret)
    except:
        new_ret = ret
    return new_ret
