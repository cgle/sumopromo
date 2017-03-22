from wtforms import StringField, IntegerField, BooleanField, DateTimeField, FloatField, TextAreaField, SelectField
from wtforms import validators as vl

from web.core.forms.common import BaseForm
from web.core.forms.common import get_current_user_businesses
from web.core.forms.fields import TagListField, WebsiteField

from web import db

#
# SUMO PROMOTION
#

class PromotionForm(BaseForm):

    business_id = SelectField('Business', choices=[])
    name = StringField('Name', [vl.InputRequired()])
    description = TextAreaField('Description', [vl.InputRequired()])
    tags = TagListField('Tags', [vl.InputRequired()])
    start_at = DateTimeField('Start time', format='%Y-%m-%d %H:%M:%S')
    end_at = DateTimeField('End time', [vl.Optional()], format='%Y-%m-%d %H:%M:%S')
    offer_price = FloatField('Offer price', [vl.Optional()])
    original_price = FloatField('Original price', [vl.Optional()])
    discount_percent = FloatField('Discount %', [vl.Optional(), vl.NumberRange(min=1, max=100)])
    total_quantity = IntegerField('Total quantity', [vl.Optional()])
    max_quantity_per_person = IntegerField('Max quantity per person', [vl.InputRequired()], default=1)
    is_activated = BooleanField('Activate', default=True)

    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business', None)    
        super(PromotionForm, self).__init__(*args, **kwargs)
        if business:
            self.business_id.choices = [(str(business.id), business.name)]
        else:
            self.business_id.choices = get_current_user_businesses()
    
    def validate_offer_price(self, field):
        if field.data and field.data <= 0:
            raise vl.ValidationError('Offer price must be greater than zero')

    def validate_original_price(self, field):
        if field.data and field.data <= 0:
            raise vl.ValidationError('Offer value must be greater than zero')     
        if field.data and self.offer_price.data and field.data <= self.offer_price.data:
            raise vl.ValidationError('Original price must be greater than offer price')

    def validate_discount_value(self, field):
        if field.data and field.data <= 0:
            raise vl.ValidationError('Offer price must be greater than zero')

#       
# INTERNET DEAL
#

class InternetDealForm(BaseForm):

    business_id = SelectField('Business', choices=[])
    name = StringField('Name', [vl.InputRequired()])
    description = TextAreaField('Description', [vl.InputRequired()])
    tags = TagListField('Tags', [vl.InputRequired()])    
    url = WebsiteField('URL', [vl.InputRequired(), vl.Length(max=2000)])
    promo_code = StringField('Promo  code', [vl.Optional()])
    start_at = DateTimeField('Start time', format='%Y-%m-%d %H:%M:%S')
    end_at = DateTimeField('End time', [vl.Optional()], format='%Y-%m-%d %H:%M:%S')
    
    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business', None)     
        super(InternetDealForm, self).__init__(*args, **kwargs)
        if business:
            self.business_id.choices = [(str(business.id), business.name)]
        else:
            self.business_id.choices = get_current_user_businesses()        
