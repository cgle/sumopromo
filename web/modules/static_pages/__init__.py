from flask import Blueprint
bp = Blueprint('static_pages', __name__)
from web.modules.static_pages.views import *
