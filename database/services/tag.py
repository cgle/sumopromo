from database.models import Tag
from database.services import DBService, DBServiceError

class TagDBService(DBService):
    
    name = 'tag'
    Model = Tag

    def create_from_list(self, tag_list):
        return [self.get_or_create(name=tag) for tag in tag_list] 
