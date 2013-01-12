# -*- encoding:utf-8 -*-
from flask import Flask
import sys
from hello.views.frontend import frontend
from hello.helpers.utils import get_cookie

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.register_module(frontend)
app.register_module(frontend,url_prefix='/test/')
app.debug = True

# init request
app.config['cookie'] = get_cookie()
