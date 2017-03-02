from database.models import User
from database.services import DBService, DBServiceError

class UserDBService(DBService):

    name = 'user'
    Model = User    

    def get_by_email(self, email):
        return self.db.query(User).filter_by(email=email).first()

    def update_by_email(self, email, **kwargs):
        user = self.get_user_by_email(email)
        if not user:
            raise DBServiceError('User {} not found'.format(email))

        user.update(**kwargs)
        self.db.commit()
        return user
    
    def delete_by_email(self, email):
        user = self.get_user_by_id(email)
        if not user:
            raise DBServiceError('User {} not found'.format(email))

        self.db.session.delete(user)
        self.db.commit()
