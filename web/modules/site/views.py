from flask import render_template
from web.modules.site import bp

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
    return render_template('site/index.html')


