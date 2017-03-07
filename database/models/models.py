import bcrypt
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Float, UnicodeText, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY

from database import Model, metadata
from database.models.enums import days_of_week_enum, business_types_enum
from database.models.types import GUID
from database.models.mixins import UpdateMixin, ModelMixin, UserMixin

from sqlalchemy_utils.types import TSVectorType

########### 

PW_HASH_ROUNDS = 12

class User(Model, UpdateMixin, ModelMixin, UserMixin):

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

    businesses = relationship('Business', backref='merchant')

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

class Business(Model, UpdateMixin, ModelMixin):

    __tablename__ = 'business'

    name = Column(String(512), nullable=False)
    type = Column(business_types_enum, default='sumo_business')

    logo = Column(String(2048))
    description = Column(UnicodeText, nullable=False)
    categories = Column(ARRAY(String))
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
    promotions = relationship('Promotion', backref='business')

    search_vector = Column(TSVectorType('name', 'description'))

    @hybrid_property
    def full_address(self):
        state = self.state if self.state != 'N/A' else ''
        return ', '.join([self.address, self.city, self.state, self.country, self.zipcode])   

#############
# PROMOTION #
#############

class Promotion(Model, UpdateMixin, ModelMixin):
    
    __tablename__ = 'promotion'
    
    business_id = Column(GUID, ForeignKey('business.id'))
    name = Column(String(255), nullable=False)
    description = Column(UnicodeText)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    tags = Column(ARRAY(String))
    type = Column(String(50))
    is_live = Column(Boolean, default=False)    

    search_vector = Column(TSVectorType('name', 'description'))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'promotion'
    }
    
    @hybrid_property
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 'Never expires'


    @hybrid_property
    def time_left(self):
        if self.end_time:
            now = datetime.now()
            start = max(now, self.start_time)
            delta = self.end_time - start
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
    def discount_pct(self):
        if self.discount:
            return '{}% OFF'.format(int(self.discount * 100))
        return None
    
    @hybrid_property
    def original_price(self):
        return self.price / (1-self.discount)

    @hybrid_property
    def is_live(self):
        raise NotImplementedError

    @hybrid_property
    def currency(self):
        return '$'

class InternetDeal(Promotion):
    
    __tablename__ = 'internet_deal'
    
    id = Column(GUID, ForeignKey('promotion.id'), primary_key=True)
    url = Column(String(2083), nullable=False)
    discount = Column(Float)
    promo_code = Column(String(512))

    __mapper_args__ = {'polymorphic_identity': 'internet_deal'}

    @hybrid_property
    def is_live(self):
        now = datetime.now()        
        if now < self.start_time:
            return False
        if self.time_left:
            return True
        return False

class SumoPromotion(Promotion):
    
    __tablename__ = 'sumo_promotion'

    id = Column(GUID, ForeignKey('promotion.id'), primary_key=True)
    price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    total_quantity = Column(Integer)
    max_coupons_per_person = Column(Integer, nullable=False, default=1)
    is_activated = Column(Boolean, default=False)

    __mapper_args__ = {'polymorphic_identity': 'sumo_promotion'}

    @hybrid_property
    def is_live(self):
        now = datetime.now()
        if now < self.start_time:
            return False
        if self.time_left and self.is_activated:
            return True
        return False

class SumoCoupon(Model, UpdateMixin, ModelMixin):
    
    __tablename__ = 'sumo_coupon'
    
    promotion_id = Column(GUID, ForeignKey('promotion.id'))
    claimer_id = Column(GUID, ForeignKey('user.id'))
    claimed_at = Column(DateTime, default=datetime.now())
    confirmed_at = Column(DateTime)
    is_valid = Column(Boolean, default=True)

