from flask import render_template
from web.modules.search import bp

@bp.route('/search')
def main():
    return render_template('search/main.html')

@bp.route('/category/<category>')
def category(category):
    return render_template('search/category.html')
