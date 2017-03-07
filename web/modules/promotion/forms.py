from wtforms import StringField, IntegerField, BooleanField, DateTimeField, FloatField, TextAreaField
from wtforms import validators as vl

from web.core.forms.common import BaseForm
from web.core.forms.fields import TagListField, PercentField

class BasePromotionForm(BaseForm):
    name = StringField('Name', [vl.InputRequired()])
    description = TextAreaField('Description', [vl.InputRequired()])
    tags = TagListField('Tags', [vl.InputRequired()])
    start_time = DateTimeField('Start time', format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField('End time', [vl.Optional()], format='%Y-%m-%d %H:%M:%S')
    price = FloatField('Price', [])
    discount = PercentField('Discount (%)', [vl.InputRequired()])
    total_quantity = IntegerField('Total quantity', [vl.Optional()])
    max_coupons_per_person = IntegerField('Max coupons per person', [vl.InputRequired()], default=1)
    is_activated = BooleanField('Activate', default=True)
    
    def validate_end_time(self, field):        
        if field.data and field.data <= self.start_time.data:
            raise vl.ValidationError('End time must be greater than start time')        

class CreatePromotionForm(BasePromotionForm):
    pass

class EditPromotionForm(BasePromotionForm):
    pass
