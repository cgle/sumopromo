from flask import Blueprint
from flask import render_template

from web.modules.static_pages import bp

@bp.route('/about')
def index():
    return render_template('static_pages/about.html')

@bp.route('/contact', methods=['GET'])
def contact():
    return render_template('static_pages/contact.html')

@bp.route('/privacy')
def privacy():
    return render_template('static_pages/privacy.html')    


