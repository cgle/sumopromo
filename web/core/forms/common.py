from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms import validators as vl
from web.misc.geo import country_names, us_states

def flatten(d):
    items = []
    for k, v in d.items():
        if type(v) == dict:
            items.extend(flatten(v).items())
        else:
            items.append((k, v))
    return dict(items)

class BaseForm(FlaskForm):
    
    @property
    def flat_data(self):
        return flatten(self.data)

class AddressForm(BaseForm):
    address = StringField('Address', [vl.InputRequired()])
    country = SelectField('Country',  [vl.InputRequired()], choices=country_names, default='US')
    city = StringField('City',  [vl.InputRequired()])
    state = SelectField('State',  [vl.InputRequired()], choices=us_states)
    zipcode = StringField('Zipcode',  [vl.InputRequired()])

class SocialForm(BaseForm):
    facebook = StringField('Facebook', [])
    twitter = StringField('Twitter', [])    
    google = StringField('Google+', [])
    youtube = StringField('Youtube', [])
    snapchat = StringField('Snapchat', [])
    yelp = StringField('Yelp', [])

#
# DB calls to populate sql query fields
#
from web import db
from flask_login import current_user

def get_current_user_businesses():
    try:
        return [(str(b.id), b.name) for b in db.business.get_by_merchant(current_user.id)] 
    except:
        return []

def create_tags(l):
    try:
        return db.tag.create_from_list(l)
    except:
        return []

def create_categories(l):
    try:
        return db.category.create_from_list(l)
    except:
        return []
