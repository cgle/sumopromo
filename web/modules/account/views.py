import ujson
from flask import abort, current_app, request, render_template, redirect, url_for, flash, session
from flask_login import login_required, logout_user, login_user, current_user
from rauth import OAuth2Service
from werkzeug import secure_filename

from web import login_manager, db, s3, s3_buckets
from web.modules.account import bp
from web.modules.account.forms import LoginForm, RegisterForm, EditAccountForm, ChangePasswordForm

#
# with email & password
#

@login_manager.user_loader
def load_user(id):
    return db.user.get_by_id(id)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.user.get_by_email(email)

        if not user:
            return redirect(url_for('account.login'))

        if user.check_password(password):
            login_user(user)
            return redirect(url_for('site.index'))

    return render_template('account/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = db.user.get_by_email(email)
        
        if user:
            return redirect(url_for('account.login'))
        
        user = db.user.add(email=email, password=password, first_name=first_name, last_name=last_name)
        login_user(user, True)

        return redirect(url_for('site.index'))
    
    return render_template('account/register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.index'))

#
# OAuth
#

@bp.route('/auth/<provider>')
def oauth_authorize(provider):
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@bp.route('/auth/<provider>/callback')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('site.index'))

    oauth = OAuthSignIn.get_provider(provider)    
    profile = oauth.callback()
    
    if profile is None:
        return redirect(url_for('account.login'))
    
    user = db.user.get_by_email(profile['email'])
    if not user:
        user = db.add(email=profile['email'], first_name=profile['first_name'], last_name=profile['last_name'])

    login_user(user, True)

    return redirect(url_for('site.index'))

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        raise NotImplementedError

    def callback(self):
        raise NotImplementedError
    
    @staticmethod
    def normalize(data):
        return data

    def get_callback_url(self):
        return url_for('account.oauth_callback', provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

#
# Google OAuth
#

class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            base_url='https://accounts.google.com'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='profile email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None
        
        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            },
            decoder=ujson.loads
        )
                
        data = ujson.loads(oauth_session.get('https://www.googleapis.com/oauth2/v2/userinfo').text)
        profile = self.normalize(data)
        return profile

    @staticmethod
    def normalize(data):
        return {
            'email': data['email'],
            'first_name': data['given_name'],
            'last_name': data['family_name'],
            'profile_pic': data['picture'],
            'social_id': 'google${}'.format(data['id'])
        }

#
# Facebook OAuth
#

class FacebookSignIn(object):
    pass

#
# Account
#

@bp.route('/my-account')
@login_required
def my_account():
    return render_template('account/my-account.html')

@bp.route('/my-account/edit', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = EditAccountForm(obj=current_user)
    if form.validate_on_submit():
        data = form.flat_data
        profile_pic = data.pop('profile_pic')
        
        if profile_pic.filename:
            filename = '{}/profile_pic/{}'.format(current_user.id, secure_filename(profile_pic.filename))
            profile_pic_url = s3.upload_file(profile_pic, filename, s3_buckets['user'])
            data['profile_pic'] = profile_pic_url

        current_user.update(**data)

        db.commit()
        return redirect(url_for('account.my_account'))

    return render_template('account/edit-account.html', form=form)

@bp.route('/my-account/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        db.user.update_one(current_user, password=form.new_password.data) 
        return redirect(url_for('account.my_account'))

    return render_template('account/change-password.html', form=form)
