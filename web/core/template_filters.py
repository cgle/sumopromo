import re
from web import app

@app.template_filter('url_args_fmt')
def format_url_args(url, **kwargs):
    new_url = ''.join([url, '?', '&'.join(['{}={}'.format(k,v) for k,v in kwargs.items()]) ])
    return new_url  

@app.template_filter('fmt_text')
def format_text(value):
    return re.sub('[^a-zA-Z0-9 \n\.]', ' ', value)

@app.template_filter('p_fmt')
def p_fmt(value, limit=200):
    if value:
        value = value[:limit]
        return value if len(value) < limit else '{}...'.format(value)

    return value

@app.template_filter('datetime_fmt')
def format_datetime(value, format='medium'):
    if not value:
        return ''
    if format == 'full':
        format="%m/%d/%y %H:%M:%S"
    elif format == 'medium':
        format="%m/%d/%y %H:%M"
    return value.strftime(format)

@app.template_filter('discount_pct_fmt')
def format_discount_pct(value):
    return '{}% OFF'.format(value)

@app.template_filter('float_fmt')
def format_float(value, digits=2):
    if value:
        return '{0:.2f}'.format(value)
    return value
 
@app.template_filter('google_map_url')
def create_google_map_url(address):
    return 'https://www.google.com/maps/embed/v1/place?key={}&q={}'.format(app.config['GOOGLE_MAP_API_KEY'], address)

@app.template_filter('google_qr_url')
def create_google_qr_code_url(value, height=512, width=512):
    return 'https://chart.googleapis.com/chart?cht=qr&chl={value}&chs={width}x{height}&choe=UTF-8&chld=L|2'.format(value=value, height=height, width=width)

