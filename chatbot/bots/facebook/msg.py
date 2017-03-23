import ujson

from chatbot.config import config
from chatbot.misc.utils import to_http_request

PATH_PREFIX = 'https://graph.facebook.com/v2.6/me/'
PAGE_ACCESS_TOKEN = config.social['facebook']['page_access_token']
URL_ = PATH_PREFIX + '{service}?access_token=' + PAGE_ACCESS_TOKEN

get_url = lambda service: URL_.format(service=service)

class Attachment(object):

    __slots__ = ('attachment_type', 'payload',)

    def to_dict(self):
        return {
            'type': self.attachment_type,
            'payload': self.payload
        }

class ImageAttachment(Attachment):

    __slots__ = ('_url',)
    attachment_type = 'image'

    def __init__(self, url):
        self._url = url

    @property
    def payload(self):
        return {
            'url': self._url
        }

class FileAttachment(Attachment):

    __slots__ = ('_url',)
    attachment_type = 'file'

    def __init__(self, url):
        self._url = url

    @property
    def payload(self):
        return {
            'url': self._url
        }

class AudioAttachment(Attachment):

    __slots__ = ('_url',)
    attachment_type = 'audio'

    def __init__(self, url):
        self._url = url

    @property
    def payload(self):
        return {
            'url': self._url
        }

class VideoAttachment(Attachment):

    __slots__ = ('_url',)
    attachment_type = 'video'

    def __init__(self, url):
        self._url = url

    @property
    def payload(self):
        return {
            'url': self._url
        }

class TemplateAttachment(Attachment):

    __slots__ = ('template',)
    attachment_type = 'template'

    def __init__(self, template):
        self.template = template

    @property
    def payload(self):
        return self.template.to_dict()

class GenericTemplate(object):

    __slots__ = ('_elements',)
    template_type = 'generic'

    def __init__(self, elements):
        if not isinstance(elements, list):
            raise ValueError('elements should be a list of Element')
        self._elements = elements

    @property
    def elements(self):
        if len(self._elements) > 10:
            raise ValueError('Too many elements in the template')
        return self._elements

    def to_dict(self):
        return {
            'template_type': self.template_type,
            'elements': [ element.to_dict() for element in self.elements ]
        }

class ButtonTemplate(object):

    __slots__ = ('text','buttons',)
    template_type = 'button'

    def __init__(self, text, buttons):
        self.text = text
        if not isinstance(buttons, list):
            raise ValueError('buttons should be a list of Button')
        self.buttons = buttons

    def to_dict(self):
        return {
            'template_type': self.template_type,
            'text': self.text,
            'buttons': [ button.to_dict() for button in self.buttons ]
        }

class Element(object):

    __slots__ = ('_title', '_subtitle', 'image_url', 'default_action', 'buttons')

    def __init__(self, title, image_url=None, default_action=None, subtitle=None, buttons=None):
        self._title = title
        self._subtitle = subtitle        
        self.image_url = image_url
        self.default_action = default_action
        self.buttons = buttons

    @property
    def title(self):
        if len(self._title) > 45:
            raise ValueError('Element.title has more than 45 characters')
        return self._title

    @property
    def subtitle(self):
        if self._subtitle:
            if len(self._subtitle) > 80:
                raise ValueError('Element.subtitle has more than 80 characters')
        return self._subtitle

    def to_dict(self):
        data = {
            'title': self.title,
            'image_url': self.image_url,
            'subtitle': self.subtitle,
            'default_action': self.default_action.to_dict()
        }
        if self.buttons:
            data['buttons'] = [ button.to_dict() for button in self.buttons ]
        return data

class Button(object):

    __slots__ = ('title',)
    button_type = None

    def __init__(self, title):
        if len(title) > 20:
            raise ValueError('Button title limit is 20 characters')
        self.title = title

    def to_dict(self):
        data = {'type': self.button_type}
        if len(self.title):
            data['title'] = self.title

        if self.button_type == 'web_url':
            data['url'] = self.url
        elif self.button_type == 'postback':
            data['payload'] = self.payload
        return data

class WebUrlButton(Button):

    __slots__ = ('url',)
    button_type = 'web_url'

    def __init__(self, title, url):
        self.url = url
        super(WebUrlButton, self).__init__(title=title)

class PostbackButton(Button):

    __slots__ = ('payload',)
    button_type = 'postback'

    def __init__(self, title, payload):
        self.payload = payload
        super(PostbackButton, self).__init__(title=title)

class QuickReplyItem(object):

    __slots__ = ('content_type', 'title', 'payload', 'image_url',)

    def __init__(self, content_type, title=None, payload=None, image_url=None):
        if content_type == 'text':
            if not title and not payload:
                raise ValueError('<Message> must be set')

        if len(title) > 20:
            raise ValueError('Quick reply title limit is 20 characters')

        if len(payload) > 1000:
            raise ValueError('Quick reply payload limit is 1000 characters')

        self.content_type = content_type
        self.title = title
        self.payload = payload
        self.image_url = image_url

    def to_dict(self):
        if self.content_type == 'location':
            return {
                'content_type': self.content_type,
                'image_url': self.image_url
            }
        if self.content_type == 'text':
            return {
                'content_type': self.content_type,
                'title': self.title,
                'payload': self.payload,
                'image_url': self.image_url
            }

class QuickReplies(object):

    __slots__ = ('_quick_replies',)

    def __init__(self, quick_replies):
        if not isinstance(quick_replies, list):
            raise ValueError('quick_replies should be a list of QuickReplyItems')
        self._quick_replies = quick_replies

    def to_dict(self):
        return [quick_reply.to_dict() for quick_reply in self._quick_replies]

class Message(object):

    __slots__ = ('text', 'attachment', 'quick_replies',)

    def __init__(self, text=None, attachment=None, quick_replies=None):
        if not text and not attachment:
            raise ValueError('<Fb message> text or attachment must be set')
        self.text = text
        self.attachment = attachment
        self.quick_replies = quick_replies

    def to_dict(self):
        data = {}
        if self.text:
            data['text'] = self.text
        if self.attachment:
            data['attachment'] = self.attachment.to_dict()
        if self.quick_replies:
            data['quick_replies'] = self.quick_replies.to_dict()
        return data

class Recipient(object):

    __slots__ = ('recipient_id', 'phone_number',)

    def __init__(self, recipient_id=None, phone_number=None):
        if not recipient_id and not phone_number:
            raise ValueError('<Recipient> id or phone_number must be set')
        self.recipient_id = recipient_id
        self.phone_number = phone_number

    def to_dict(self):
        if self.recipient_id:
            return {'id': self.recipient_id}
        return {'phone_number': self.phone_number}

class MsgRequest(object):

    __slots__ = ()
    URL = None

    def to_dict(self):
        raise NotImplementedError

    def to_http_request(self, **kwargs):
        return to_http_request(self.URL, self.to_dict(), **kwargs)

class MessageRequest(MsgRequest):

    __slots__ = ('recipient','message','_notification_type',)    
    URL = get_url('messages')
    NOTIFICATION_TYPE_OPTIONS = ('REGULAR', 'SILENT_PUSH', 'NO_PUSH')

    def __init__(self, recipient, message, notification_type=None):
        self.recipient = recipient
        self.message = message
        self._notification_type = notification_type

    @property
    def notification_type(self):
        if self._notification_type:
            if self._notification_type not in self.NOTIFICATION_TYPE_OPTIONS:
                raise ValueError(
                    'notification_type valid options: %s' %
                    str(self.NOTIFICATION_TYPE_OPTIONS)
                )
        return self._notification_type

    def to_dict(self):
        data = {
            'recipient': self.recipient.to_dict(),
            'message': self.message.to_dict()
        }
        if self.notification_type:
            data['notification_type'] = self.notification_type
        return data

class SettingRequest(MsgRequest):

    URL = get_url('thread_settings')

    def __init__(self, setting_type=None, **kwargs):
        self.settings = kwargs
        self.settings['setting_type'] = setting_type

    def to_dict(self):
        return self.settings

