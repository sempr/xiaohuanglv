# -*- encoding:utf-8 -*-
from flask import Flask
import sys
from xiaohuanglv.views.frontend import frontend
from xiaohuanglv.helpers.utils import get_cookie

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.register_blueprint(frontend)
app.debug = True

# init request
app.config['cookie'] = get_cookie()
