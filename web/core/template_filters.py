import re
from web import app

@app.template_filter('fmt_text')
def format_text(value):
    return re.sub('[^a-zA-Z0-9 \n\.]', ' ', value)

@app.template_filter('datetime')
def format_datetime(value, format='medium'):
    if format == 'full':
        format="%m/%d/%y %H:%M:%S"
    elif format == 'medium':
        format="%m/%d/%y %H:%M"
    return value.strftime(format)


@app.template_filter('float_fmt')
def format_float(value, digits=2):
    return "{0:.2f}".format(value)
 
@app.template_filter('google_map_url')
def create_google_map_url(address):
    return 'https://www.google.com/maps/embed/v1/place?key={}&q={}'.format(app.config['GOOGLE_MAP_API_KEY'], address)
