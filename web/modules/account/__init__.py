from flask import Blueprint
bp = Blueprint('account', __name__)

from web.modules.account.views import *
