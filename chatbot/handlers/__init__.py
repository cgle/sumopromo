def init_handlers():
    from chatbot.handlers.pages import handlers as pages
    from chatbot.handlers.webhooks import handlers as webhooks
    return pages + webhooks
