from database.models import Business
from database.services import DBService, DBServiceError

class BusinessDBService(DBService):
    
    name = 'business'
    Model = Business

    def create(self, merchant_id, **kwargs):
        if self.filter_by(name=kwargs['name'], merchant_id=merchant_id):
            raise DBServiceError('duplicate business for same merchant')
        
        business = Business()
        business.merchant_id = merchant_id
        business.update(**kwargs)

        self.db.session.add(business)
        self.db.commit()

        return business

    def get_by_merchant(self, merchant_id):
        businesses = self.db.query(Business).filter_by(merchant_id=merchant_id).all()
        return businesses    
    
    def get_promotions(self, business_id):
        business = self.get_by_id(business_id)
        if not business:
            raise DBServiceError('Business {} not found'.format(business_id))

        promotions = business.promotions
        return promotions

    def add_follower(self, business_id, user):
        business = self.get_by_id(business_id)
        if not business:
            raise DBServiceError('Business {} not found'.format(business_id))
        business.followers.append(user)
        self.db.commit()
        return business
