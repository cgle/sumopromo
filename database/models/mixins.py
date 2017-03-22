import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from database.models.types import GUID

class ModelMixin(object):
    
    id = Column(GUID, default=uuid.uuid4, primary_key=True)

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

class CreatedAtMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)    

class UpdatedAtMixin(object):
    updated_at = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

class UpdateMixin(object):
   
    def update(self, **kwargs):
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

class UserMixin(object):

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal    
