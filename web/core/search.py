from flask_login import current_user
from sqlalchemy_searchable import parse_search_query

from web import db

def current_user_nearby_promotions():
    #TODO implement this
    return db.promotion.get_all()

def current_user_nearby_businesses():
    #TODO implement this
    return db.business.get_all()

biz_and_promo_vector = db.promotion.Model.search_vector | db.business.Model.search_vector | db.tag.Model.search_vector | db.category.Model.search_vector

def find_promotions(query, limit=None):
    promotions = (db.promotion.query().join(db.business.Model)
                                      .join(db.business.Model.tags, db.business.Model.categories)
                                      .filter(
                                         biz_and_promo_vector.match(parse_search_query(query))
                                     ).all())
    return promotions

def find_businesses(query, limit=None):
    businesses = (db.business.query().join(db.promotion.Model)
                                      .join(db.promotion.Model.tags, db.promotion.Model.categories)
                                     .filter(
                                         biz_and_promo_vector.match(parse_search_query(query))
                                     ).all())
    return businesses
