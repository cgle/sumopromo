import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from flask import Flask, _app_ctx_stack
from flask_compress import Compress
from flask_login import LoginManager
from flask_assets import Bundle, Environment

import config.web
from config.db import database_uri, session_options, engine_options
from config.aws import aws_config

from database import metadata
from database.sumodb import SumoDB

from drivers.s3 import S3Manager

basedir = os.path.dirname(os.path.realpath(__file__))
location = lambda x: os.path.join(basedir, x)

##########
# CONFIG #
##########

app = Flask(__name__, 
            static_url_path='/static',
            static_folder=location('static'), 
            template_folder=location('templates')
           )

app.config.from_object(config.web.DevConfig)
app.url_map.strict_slashes = False

#########################
# SETUP UPLOAD SERVICES #
#########################

s3 = S3Manager(aws_secret_access_key=aws_config['secret_access_key'],
               aws_access_key_id=aws_config['access_key_id'])

s3_buckets = app.config['S3_BUCKETS']
s3.setup_buckets(s3_buckets.values())

@app.teardown_appcontext
def close_s3(resp_or_exc=None):
    return resp_or_exc

############
# SETUP DB #
############

db = SumoDB(database_uri, metadata=metadata, 
            engine_options=engine_options, session_options=session_options,
            scopefunc=_app_ctx_stack.__ident_func__)

@app.teardown_appcontext
def shutdown_session(response_or_exc=None):
    if db.session:
        db.session.remove()
    return response_or_exc

####################
# SETUP EXTENSIONS #
####################

gzip = Compress(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "account.login"

#################
# IMPORT ASSETS #
#################

assets = Environment(app)

#
# JS
#

vendor_js = Bundle(location('assets/vendor/jquery-3.1.1.min.js'), filters='jsmin', output='js/vendor.js')
global_js = Bundle(location('assets/js/layout.js'), filters='jsmin', output='js/global.js')
assets.register('vendor_js', vendor_js)
assets.register('global_js', global_js)

#
# CSS
#

site_css = Bundle(location('assets/less/site.less'),depends=['less/*.less'], filters='less,cssmin', output='css/site.css')
assets.register('site_css', site_css)


######################
# IMPORT BLUEPRINTS  #
######################
from web import app
from web.modules.main import bp as main
from web.modules.static_pages import bp as static_pages
from web.modules.account import bp as account
from web.modules.business import bp as business
from web.modules.promotion import bp as promotion

app.register_blueprint(main)
app.register_blueprint(static_pages)
app.register_blueprint(account)
app.register_blueprint(business)
app.register_blueprint(promotion)
