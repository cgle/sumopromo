from flask import Blueprint
bp = Blueprint('promotion', __name__)
from web.modules.promotion.views import *
