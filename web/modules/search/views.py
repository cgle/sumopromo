from flask import render_template, request
from web.modules.search import bp
from web.core import search

@bp.route('/search')
def main():
    query = request.args.get('query', '')
    promotions = search.find_promotions(query)
    businesses = set([promotion.business for promotion in promotions])
    return render_template('search/main.html', promotions=promotions, businesses=businesses, query=query)

@bp.route('/category/<category>')
def category(category):
    return render_template('search/category.html')
