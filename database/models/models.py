import bcrypt
from datetime import datetime, timedelta

from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Float, UnicodeText, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from database import Model, metadata
from database.models.enums import days_of_week_enum, business_types_enum
from database.models.types import GUID, CastingArray
from database.models.mixins import  ModelMixin, CreatedAtMixin, UpdatedAtMixin, UserMixin

from sqlalchemy_utils.types import TSVectorType

from utils.string_utils import get_alpha_ID

########### 

PW_HASH_ROUNDS = 12

user_follow_business_table = Table('user_follow_business', metadata,
    Column('user_id', GUID, ForeignKey('user.id')),
    Column('business_id', GUID, ForeignKey('business.id')),
    Column('created_at', DateTime, default=datetime.now)
)

user_promotion_watchlist_table = Table('user_promotion_watchlist', metadata,
    Column('user_id', GUID, ForeignKey('user.id')),
    Column('promotion_id', GUID, ForeignKey('promotion.id')),
    Column('created_at', DateTime, default=datetime.now)
)

class User(Model, ModelMixin, CreatedAtMixin, UpdatedAtMixin, UserMixin):

    __tablename__ = 'user'
    
    email = Column(String(255), unique=True, nullable=False)    
    _password = Column(String(255))

    first_name = Column(String(128), default='')
    last_name = Column(String(128), default='')
    profile_pic = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    country = Column(String(10), default='US')
    zipcode = Column(String(20))
    social_accounts = Column(JSONB)

    businesses = relationship('Business', backref='merchant')    
    following = relationship('Business', secondary=user_follow_business_table, backref='followers')
    watchlist = relationship('Promotion', secondary=user_promotion_watchlist_table, backref='watchers')

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name            
    
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, password):
        self._password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(PW_HASH_ROUNDS)).decode('utf8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self._password.encode('utf8'))

############
# BUSINESS #
############

business_to_category_table = Table('business_to_category', metadata,
    Column('business_id', GUID, ForeignKey('business.id')),
    Column('category_id', GUID, ForeignKey('category.id'))
)

business_to_tag_table = Table('business_to_tag', metadata,
    Column('business_id', GUID, ForeignKey('business.id')),
    Column('tag_id', GUID, ForeignKey('tag.id'))
)

class Category(Model, ModelMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = 'category'
    name = Column(String(200))
    search_vector = Column(TSVectorType('name'))

class Tag(Model,  ModelMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = 'tag'
    name = Column(String(200))    
    search_vector = Column(TSVectorType('name'))

class Business(Model, ModelMixin, CreatedAtMixin, UpdatedAtMixin):

    __tablename__ = 'business'

    name = Column(String(512), nullable=False)
    type = Column(business_types_enum, default='sumo_business')

    logo = Column(String(2048))
    description = Column(UnicodeText, nullable=False)
    categories = relationship('Category', secondary=business_to_category_table, backref='businesses')
    tags = relationship('Tag', secondary=business_to_tag_table, backref='businesses')
    website = Column(String(512))
    email = Column(String(512), nullable=False)
    phone = Column(String(50), nullable=False)
    fax = Column(String(50))
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False, default='NA')
    country = Column(String(10), nullable=False, default='US')
    zipcode = Column(String(20), nullable=False)

    facebook = Column(String(512))
    google = Column(String(512))
    youtube = Column(String(512))
    twitter = Column(String(512))
    snapchat = Column(String(512))
    yelp = Column(String(512))

    merchant_id = Column(GUID, ForeignKey('user.id'))
    promotions = relationship('Promotion', backref='business', cascade="all, delete-orphan")

    search_vector = Column(TSVectorType('name', 'description'))

    @hybrid_property
    def full_address(self):
        state = self.state if self.state != 'N/A' else ''
        return ', '.join([self.address, self.city, self.state, self.country, self.zipcode])


    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': str(self.description),
            'type': self.type,
            'logo': self.logo,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'zipcode': self.zipcode,
            'website': self.website,
            'email': self.email,
            'phone': self.phone
        }

#############
# PROMOTION #
#############

promotion_to_tag_table = Table('promotion_to_tag', metadata,
    Column('promotion_id', GUID, ForeignKey('promotion.id')),
    Column('tag_id', GUID, ForeignKey('tag.id'))
)

class Promotion(Model, ModelMixin, CreatedAtMixin, UpdatedAtMixin):
    
    __tablename__ = 'promotion'
    
    business_id = Column(GUID, ForeignKey('business.id'))
    name = Column(String(255), nullable=False)
    description = Column(UnicodeText, nullable=False)    
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    extras = Column(JSONB)

    tags = relationship('Tag', secondary=promotion_to_tag_table, backref='promotions')

    type = Column(String(50))

    search_vector = Column(TSVectorType('name', 'description'))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'promotion'
    }
    
    @hybrid_property
    def is_sumo(self):
        return self.type == 'sumo_promotion'

    @hybrid_property
    def is_internet_deal(self):
        return self.type == 'internet_deal'
    
    @hybrid_property
    def duration(self):
        if self.start_at and self.end_at:
            return self.end_at - self.start_at
        return 'Never expires'

    @hybrid_property
    def time_left(self):
        if self.end_at:
            now = datetime.now()
            start = max(now, self.start_at)
            delta = self.end_at - start
            delta_secs = delta.total_seconds()
            if delta_secs < 0:
                return 0
            return delta_secs

        # never expires
        return float('inf')

    @hybrid_property
    def time_left_str(self):
        ds = self.time_left
        if ds == float('inf'):
            return 'Infinity'
        
        delta = timedelta(seconds=int(ds))
        return str(delta)            

    @hybrid_property
    def is_live(self):
        raise NotImplementedError

    @hybrid_property
    def currency(self):
        return '$'

user_to_internet_deal_table = Table('user_to_internet_deal', metadata,
    Column('user_id', GUID, ForeignKey('user.id')),
    Column('internet_deal_id', GUID, ForeignKey('internet_deal.id'))
)

class InternetDeal(Promotion):
    
    __tablename__ = 'internet_deal'
    
    id = Column(GUID, ForeignKey('promotion.id'), primary_key=True)
    url = Column(String(2083), nullable=False)
    promo_code = Column(String(512))

    users = relationship('User', secondary=user_to_internet_deal_table, backref='internet_deals')

    __mapper_args__ = {'polymorphic_identity': 'internet_deal'}

    @hybrid_property
    def is_live(self):
        now = datetime.now()        
        if now < self.start_at:
            return False
        if self.time_left:
            return True
        return False
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'type': self.type,
            'business': self.business.to_dict(),
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'promo_code': self.promo_code,
            'is_live': self.is_live,
            'start_at': str(self.start_at),
            'end_at': str(self.end_at)
        }

class SumoPromotion(Promotion):
    
    __tablename__ = 'sumo_promotion'

    id = Column(GUID, ForeignKey('promotion.id'), primary_key=True)
    offer_price = Column(Float)
    original_price = Column(Float)
    discount_percent = Column(Float)
    total_quantity = Column(Integer)
    max_quantity_per_person = Column(Integer)
    is_activated = Column(Boolean, default=False)

    __mapper_args__ = {'polymorphic_identity': 'sumo_promotion'}

    @hybrid_property
    def is_live(self):
        now = datetime.now()
        if now < self.start_at:
            return False
        if self.time_left and self.is_activated:
            return True

        return False

    def to_dict(self):
        return {
            'id': str(self.id),
            'type': self.type,
            'business': self.business.to_dict(),
            'name': self.name,
            'description': self.description,
            'offer_price': self.offer_price,
            'original_price': self.original_price,
            'discount_percent': self.discount_percent,
            'total_quantity': self.total_quantity,
            'max_quantity_per_person': self.max_quantity_per_person,
            'is_activated': self.is_activated,
            'is_live': self.is_live,
            'start_at': str(self.start_at),
            'end_at': str(self.end_at)
        }

def generate_sumo_code(context):
    id = context.current_parameters.get('id')
    return get_alpha_ID(id.int >> 64 - 1)

class SumoVoucher(Model, ModelMixin, CreatedAtMixin, UpdatedAtMixin):
   
    __tablename__ = 'sumo_voucher'
        
    promotion_id = Column(GUID, ForeignKey('sumo_promotion.id'))
    user_id = Column(GUID, ForeignKey('user.id'))
    claimed_at = Column(DateTime, default=datetime.now)
    confirmed_at = Column(DateTime)
    sumo_code = Column(String(100), default=generate_sumo_code)

    promotion = relationship('SumoPromotion', backref='vouchers')
    user = relationship('User', backref='sumo_vouchers')

    @hybrid_property
    def is_active(self):
        return self.promotion.is_live and not self.confirmed_at        
