from config.chatbot import Config
config = Config()

import logging, signal, time
from tornado import ioloop, httpserver

def setup_uvloop():
    from chatbot.misc.uvloop import UVLoop
    ioloop.IOLoop.configure(UVLoop)

#setup_uvloop()

# import chatbot app relevant modules/libs
from chatbot.app import ChatbotApp

def register_shutdown_handler(http_server):
    shutdown_handler = lambda sig, frame: shutdown(http_server)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)


def shutdown(server_instance):
    ioloop_instance = ioloop.IOLoop.instance()
    logging.info('Stopping server gracefully.')

    server_instance.stop()

    def finalize():
        ioloop_instance.stop()
        logging.info('Server stopped.')

    # wait for 0.5 second then stop io_loop
    ioloop_instance.add_timeout(time.time() + 0.5, finalize)

def start():
    app = ChatbotApp(config.app)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(config.server['port'], config.server['host'])

    register_shutdown_handler(http_server)
    ioloop.IOLoop.current().start()
