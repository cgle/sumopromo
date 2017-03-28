from flask import Blueprint
bp = Blueprint('api', __name__)

from web.modules.api.views import *

