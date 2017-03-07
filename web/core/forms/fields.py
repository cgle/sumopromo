from wtforms import Field, FloatField
from wtforms.widgets import TextInput

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

class PercentField(FloatField):

    def _value(self):
        if self.data:
            return self.data * 100
        return 0

    def process_formdata(self, valuelist):        
        value = valuelist[0]
        self.data = float(value) / 100.0

class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return ', '.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []
