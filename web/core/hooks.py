from flask import session, request
import requests
import ujson
from web import app

'''
@app.before_request
def set_user_location():    
    if 'location' not in session:
        resp = requests.get('http://freegeoip.net/json/{}'.format(request.remote_addr))
        location_data = ujson.loads(resp.text)
        session['location'] = location_data
'''
