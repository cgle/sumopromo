from flask import Blueprint
bp = Blueprint('sumo_voucher', __name__)
from web.modules.sumo_voucher.views import *
