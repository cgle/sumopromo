from sqlalchemy import and_

class DBServiceError(Exception):
    pass

class DBService(object):

    name = 'db_service'
    Model = None

    def __init__(self, db):
        self.db = db

        if hasattr(db, self.name):
            raise AttributeError('service {} exists in db'.format(self.name))
        
        setattr(db, self.name, self)

    def add(self, **kwargs):
        item = self.Model(**kwargs)
        self.db.session.add(item)
        self.db.commit()
        return item
    
    def get_all(self, limit=100):
        return self.db.query(self.Model).limit(limit).all()
    
    def get_or_create(self, **kwargs):
        items = self.filter_by(**kwargs)
        if items:
            return items[0]
        else:
            return self.add(**kwargs)

    def filter(self, *args, **kwargs):
        limit = kwargs.pop('limit', None)
        filter_rule = and_(*args)
        return self.db.query(self.Model).filter(filter_rule).limit(limit).all()

    def filter_q(self, *args):
        filter_rule = and_(*args)
        return self.db.query(self.Model).filter(filter_rule)

    def filter_by(self, **kwargs):
        limit = kwargs.pop('limit', None)
        return self.db.query(self.Model).filter_by(**kwargs).limit(limit).all()

    def get_by_id(self, id):
        return self.db.query(self.Model).get(id)

    def update_by_id(self, id, **kwargs):
        item = self.db.query(self.Model).get(id)
        if item is None:
            raise DBServiceError('{} {} not found'.format(self.model.__name__, id))
        item.update(**kwargs)
        self.db.commit()
        return item

    def delete_by_id(self, id):
        item =self.db.query(self.Model).get(id)
        if item is None:
            raise DBServiceError('{} {} not found'.format(self.model.__name__, id))
        self.db.session.delete(item)
        self.db.commit()
    
    def update_one(self, item, **kwargs):
        item.update(**kwargs)
        self.db.commit()
        return item

    def delete_one(self, item):
        self.db.session.delete(item)
        self.db.commit()

    def search(self, *args, **kwargs):
        query = self.db.query(self.Model)
        return self.db.search(query, *args, **kwargs)

def init(db):
    from database.services.user import UserDBService
    from database.services.business import BusinessDBService
    from database.services.promotion import PromotionDBService
    from database.services.tag import TagDBService
    from database.services.category import CategoryDBService
    from database.services.sumo_voucher import SumoVoucherDBService

    services = {service.name: service for service in (
        UserDBService(db),
        BusinessDBService(db),
        PromotionDBService(db),
        TagDBService(db),
        CategoryDBService(db),
        SumoVoucherDBService(db)
    )}

    return services    
