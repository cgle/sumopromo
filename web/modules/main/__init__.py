from flask import Blueprint
bp = Blueprint('main', __name__)
from web.modules.main.views import *
