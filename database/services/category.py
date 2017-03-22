from database.models import Category
from database.services import DBService, DBServiceError

class CategoryDBService(DBService):
    
    name = 'category'
    Model = Category

    def create_from_list(self, category_list):
        categories = [self.get_or_create(name=category) for category in category_list]
        return categories

