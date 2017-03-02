from flask import Blueprint
bp = Blueprint('business', __name__)
from web.modules.business.views import *
