from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, FormField, FieldList, IntegerField
from wtforms import validators as vl

from web.core.forms.common import BaseForm, AddressForm, SocialForm
from web.core.forms.fields import TagListField

class CreateBusinessForm(BaseForm):
    name = StringField('Name', [vl.InputRequired()])
    categories = TagListField('Categories', [vl.InputRequired()])
    logo = FileField('Logo', [])
    description = TextAreaField('Description', [vl.InputRequired()])
    website = StringField('Website', [vl.Length(max=512)])
    email = StringField('Email', [vl.InputRequired(), vl.Length(max=512)])
    phone = StringField('Phone', [vl.InputRequired()])
    fax = StringField('Fax', [])
    address = FormField(AddressForm)
    social = FormField(SocialForm)
