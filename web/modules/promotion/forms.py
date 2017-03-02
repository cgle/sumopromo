from wtforms import StringField, IntegerField, BooleanField, DateTimeField, FloatField, TextAreaField
from wtforms import validators as vl

from web.core.forms.common import BaseForm
from web.core.forms.fields import TagListField

class CreatePromotionForm(BaseForm):
    name = StringField('Name', [vl.InputRequired()])
    description = TextAreaField('Description', [vl.InputRequired()])
    tags = TagListField('Tags', [vl.InputRequired()])
    start_time = DateTimeField('Start time', format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField('End time', format='%Y-%m-%d %H:%M:%S')
    price = FloatField('Price', [])
    discount = FloatField('Discount (%)', [vl.InputRequired()])
    total_quantity = IntegerField('Total quantity')
    max_coupons_per_person = IntegerField('Max coupons per person', [vl.InputRequired()], default=1)
    is_activated = BooleanField('Activate', default=True)
