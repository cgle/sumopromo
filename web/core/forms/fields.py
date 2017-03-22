from wtforms import Field, FloatField
from wtforms.widgets import TextInput
from web import db
from flask_login import current_user
from web.core.forms.common import create_tags, create_categories


class WebsiteField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return self.data
        return ''

    def process_formdata(self, valuelist):
        value = valuelist[0]
        if value.startswith('http://') or value.startswith('https://'):
            self.data = value
        else:
            self.data = 'http://{}'.format(value)

class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:    
            return ', '.join((c.name for c in self.data))
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            tag_list = [x.strip() for x in valuelist[0].split(',')]
            self.data = create_tags(tag_list)
        else:
            self.data = []

class CategoryListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return ', '.join((c.name for c in self.data))
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            category_list = [x.strip() for x in valuelist[0].split(',')]
            self.data = create_categories(category_list)
        else:
            self.data = []
