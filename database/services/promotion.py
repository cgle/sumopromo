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
        self.promo_entity = with_polymorphic(Promotion, [InternetDeal, SumoPromotion], flat=True)

    def create_sumo_promotion(self, business_id, **kwargs):
        promotion = SumoPromotion()
        promotion.business_id = business_id
        promotion.update(**kwargs)
        
        self.db.session.add(promotion)
        self.db.commit()

        return promotion
    
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
            raise DBServiceError('Promotion {} not found'.format(promotion+id))
        self.delete_one(promotion)

    def get_internet_deal_by_id(self, deal_id):
        deal = self.db.query(self.internet_deal_entity).filter_by(id=deal_id).first()
        return deal

    def create_internet_deal(self, business_id, **kwargs):
        deal = InternetDeal()
        deal.business_id = business_id
        deal.update(**kwargs)
        self.db.session.add(deal)
        self.db.commit()
        return deal

    def update_internet_deal_by_id(self, deal_id, **kwargs):
        deal = self.get_internet_deal_by_id(deal_id)
        if not deal:
            raise DBServiceError('Internet deal {} not found'.format(deal_id))

        return self.update_one(deal, **kwargs)

    def delete_internet_deal_by_id(self, deal_id):
        deal = self.get_internet_deal_by_id(deal_id)
        if not deal:
            raise DBServiceError('Internet deal {} not found'.format(deal_id))
        self.delete_one(deal)
