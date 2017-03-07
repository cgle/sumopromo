import os
import datetime
from flask import Flask, request, render_template, session, Response
from flask_compress import Compress

basedir = os.path.dirname(os.path.realpath(__file__))
location = lambda x: os.path.join(basedir, x)
app = Flask(__name__, static_url_path='/static', static_folder=location('static'))
app.secret_key = b"\xd8z\x0bI\x11I~\x1b\n\xe2\x08\xcdh\xc1\\xb6\x06\xdbO\xa3\xf4.K<"

gzip = Compress(app)

emails_filepath = location('emails.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-email', methods=['POST'])
def submit_email():
    email = request.form.get('email')
    user_type = request.form.get('user_type')
    now = datetime.datetime.now()
    
    already_submit_message = 'You already submitted your email. Thank you!'

    if 'submit_email' in session and session['submit_email'] == email:
        return already_submit_message, 500

    try:            
        f = open(emails_filepath, 'a+', encoding='utf-8')
        f.seek(0)
        s = f.read()
        if email in s:
            f.close()
            session['submit_email'] = email
            return already_submit_message, 500
    
        f.write('{},{},{}\n'.format(now,email,user_type))
        f.close()
        session['submit_email'] = email

        return 'OK', 200

    except IOError:
        return 'Error saving the email', 500

@app.route('/robots.txt')
def robotstxt():
    disallow = lambda string: 'Disallow: {0}'.format(string)
    return Response('User-agent: *\n{0}\n'.format('\n'.join([
        disallow('/bin/*'),
    ])))
