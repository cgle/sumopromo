from web import db
from flask_login import current_user

def current_user_nearby_promotions():
    #TODO implement this
    return db.promotion.get_all()

def current_user_nearby_businesses():
    #TODO implement this
    return db.business.get_all()

biz_and_promo_vector = db.promotion.Model.search_vector | db.business.Model.search_vector | db.category.Model.search_vector | db.tag.Model.search_vector

def find_promotions(query, limit=None):
    promotions = db.promotion.search(query, vector=biz_and_promo_vector)
    return promotions

def find_businesses(query, limit=None):
    businesses = db.business.search(query, vector=biz_and_promo_vector)
    return businesses
