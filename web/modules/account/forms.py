from flask_login import current_user

from wtforms import StringField, FileField, PasswordField, SelectField, FormField
from wtforms import validators as vl

from web.core.forms.common import BaseForm
from web.misc.geo import country_names, us_states

class LoginForm(BaseForm):
    email = StringField('Email', [vl.InputRequired(), vl.Email()])
    password = PasswordField('Password', [vl.InputRequired()])

class RegisterForm(BaseForm):
    email = StringField('Email', [vl.InputRequired(), vl.Email()])
    password = PasswordField('Password', [vl.InputRequired()])    
    confirm = PasswordField('Confirm password', [
        vl.InputRequired(),
        vl.EqualTo('password', message='Password must match')
    ])
    first_name = StringField('First name', [vl.InputRequired()])
    last_name = StringField('Last name', [vl.InputRequired()])
    
class EditAccountForm(BaseForm):
    first_name = StringField('First name', [vl.Length(max=50)])
    last_name = StringField('Last name', [vl.Length(max=50)])
    profile_pic = FileField('Profile picture', [])
    country = SelectField('Country',  [vl.InputRequired()], choices=country_names, default='US')
    city = StringField('City',  [vl.InputRequired()])
    state = SelectField('State',  [vl.InputRequired()], choices=us_states)
    zipcode = StringField('Zipcode',  [vl.InputRequired()])

class ChangePasswordForm(BaseForm):
    current_password = PasswordField('Current password', [vl.InputRequired()])
    new_password = PasswordField('New password', [vl.InputRequired()])
    confirm = PasswordField('Confirm password', [
        vl.InputRequired(),
        vl.EqualTo('new_password', message='Password must match')
    ])

    def validate_current_password(self, field):
        if not current_user.check_password(field.data):
            raise vl.ValidationError('Invalid current password')
