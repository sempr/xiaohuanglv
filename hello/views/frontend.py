# -*- encoding:utf-8 -*-
from flask import Module, request, render_template, current_app, Blueprint
from werkzeug.wsgi import LimitedStream

from hello.jobs.job0 import add
from hello.helpers import utils,parser

frontend = Blueprint('',__name__)

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
    content_length = request.headers.get('content-length', type=int)
    if content_length is not None:
        stream = LimitedStream(request.environ['wsgi.input'],
                               content_length)
        old_msg = stream.read()
        print old_msg
    else:
        old_msg = 'error'
    try:
        msg = parser.parse_txt(old_msg)
    except:
        msg = old_msg
    cookie = current_app.config['cookie']
    print cookie
    ret = utils.get_msg(msg,cookie)
    try:
        new_ret = parser.build_txt(old_msg,ret)
    except:
        new_ret = ret
    print new_ret
    return new_ret
