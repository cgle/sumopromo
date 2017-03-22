from tornado import web

class IndexHandler(web.RequestHandler):
    
    @web.asynchronous
    def get(self):
        self.write('Chatbot init OK')
        self.finish()
        return

handlers = [
    (r'/', IndexHandler),
]
