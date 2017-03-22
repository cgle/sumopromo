from database.models import Promotion, InternetDeal, SumoPromotion
from database.services import DBService, DBServiceError
from sqlalchemy.orm import with_polymorphic

class PromotionDBService(DBService):
    
    name = 'promotion'
    Model = Promotion

    def __init__(self, *args, **kwargs):
        super(PromotionDBService, self).__init__(*args, **kwargs)
        self.internet_deal_entity = with_polymorphic(Promotion, InternetDeal)
        self.sumo_promotion_entity = with_polymorphic(Promotion, SumoPromotion)
        self.promotion_entity = with_polymorphic(Promotion, [InternetDeal, SumoPromotion], flat=True)

    def get_promotion_by_id(self, promotion_id):
        promotion = self.db.query(self.promotion_entity).filter_by(id=promotion_id).first()
        return promotion

    def create_sumo_promotion(self, business_id, **kwargs):        
        promotion = SumoPromotion()
        promotion.business_id = business_id
        promotion.update(**kwargs)
        
        self.db.session.add(promotion)
        self.db.commit()

        return promotion
    
    def get_promotions_by_merchant(self, merchant):
        promotions = [promotion for business in merchant.businesses for promotion in business.promotions]
        return promotions

    def get_sumo_promotion_by_id(self, promotion_id):        
        promotion = self.db.query(self.sumo_promotion_entity).filter_by(id=promotion_id).first()
        return promotion

    def update_sumo_promotion_by_id(self, promotion_id, **kwargs):
        promotion = self.get_sumo_promotion_by_id(promotion_id)
        if not promotion:
            raise DBServiceError('Promotion {} not found'.format(promotion_id))

        return self.update_one(promotion, **kwargs)

    def delete_sumo_promotion_by_id(self, promotion_id):
        promotion = self.get_sumo_promotion_by_id(promotion_id)
        if not promotion:
            raise DBServiceError('Promotion {} not found'.format(promotion_id))
        self.delete_one(promotion)

    def activate_sumo_promotion(self, promotion_id):
        promotion = self.get_sumo_promotion_by_id(promotion_id)
        self.update_one(promotion, is_activated=True)
        return True

    def deactivate_sumo_promotion(self, promotion_id):
        promotion = self.get_sumo_promotion_by_id(promotion_id)
        self.update_one(promotion, is_activated=False)
        return True

    def get_internet_deal_by_id(self, promotion_id):
        deal = self.db.query(self.internet_deal_entity).filter_by(id=promotion_id).first()
        return deal

    def create_internet_deal(self, business_id, **kwargs):
        deal = InternetDeal()
        deal.business_id = business_id
        deal.update(**kwargs)
        self.db.session.add(deal)
        self.db.commit()
        return deal

    def update_internet_deal_by_id(self, promotion_id, **kwargs):
        deal = self.get_internet_deal_by_id(promotion_id)
        if not deal:
            raise DBServiceError('Internet deal {} not found'.format(promotion_id))
        return self.update_one(deal, **kwargs)

    def delete_internet_deal_by_id(self, promotion_id):
        promotion = self.get_internet_deal_by_id(promotion_id)
        if not promotion:
            raise DBServiceError('Internet deal {} not found'.format(promotion_id))
        self.delete_one(deal)

    def add_to_watchlist(self, promotion_id, user):
        promotion = self.get_promotion_by_id(promotion_id)
        if not promotion:
            raise DBServiceError('Promotion {} not found'.format(promotion_id))

        promotion.watchers.append(user)
        self.db.commit()
        return promotion

    def claim(self, user, promotion):
        # sumo promotion
        if promotion.is_sumo:
            return self.db.sumo_voucher.create_per_user(user, promotion)

        # internet deal
        if promotion.is_internet_deal:
            return self.claim_internet_deal(user, promotion)

    def claim_internet_deal(self, user, promotion):
        promotion.users.append(user)
        self.db.commit()
        return promotion
                        
