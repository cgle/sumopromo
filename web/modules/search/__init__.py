from flask import Blueprint
bp = Blueprint('search', __init__)
from web.modules.search.views import *
