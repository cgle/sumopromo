from flask import Blueprint
bp = Blueprint('site', __name__)
from web.modules.site.views import *

