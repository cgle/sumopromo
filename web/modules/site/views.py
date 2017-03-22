from flask import render_template, request, session
from web.modules.site import bp
from web.core import search

#
# STATIC PAGES
#
@bp.route('/about')
def about():
    return render_template('site/about.html')

@bp.route('/contact', methods=['GET'])
def contact():
    return render_template('site/contact.html')

@bp.route('/privacy')
def privacy():
    return render_template('site/privacy.html')    

@bp.route('/tos')
def tos():
    return render_template('site/tos.html')

@bp.route('/')
def index():
    promotions = search.current_user_nearby_promotions()
    businesses = search.current_user_nearby_businesses()
    return render_template('site/index.html', promotions=promotions, businesses=businesses)
