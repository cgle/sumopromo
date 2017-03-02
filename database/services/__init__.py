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

    def filter(self, *args, **kwargs):
        limit = kwargs.pop('limit', None)
        return self.db.query(self.Model).filter(*args).limit(limit).all()

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

def init(db):
    from user import UserDBService
    from business import BusinessDBService    
    from promotion import PromotionDBService

    services = {service.name: service for service in (
        UserDBService(db),
        BusinessDBService(db),
        PromotionDBService(db),
    )}

    return services



    
