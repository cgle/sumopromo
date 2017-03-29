import ujson
from flask import request, Response, abort

from web import db
from web.modules.api import bp
from web.core import search

def json_resp(output):
    resp = Response(ujson.dumps(output))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@bp.route('/search')
def search_api():
    query = request.args.get('query', '')
    promotions = search.find_promotions(query)
    
    output = {
        'query': query,
        'promotions': [promotion.to_dict() for promotion in promotions],
    }
    
    return json_resp(output)

@bp.route('/promos/<promotion_id>')
def view_promotion_api(promotion_id):
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    if not promotion:
        abort(500)

    output = {
        'promotion': promotion.to_dict()
    }
    return json_resp(output)
    
