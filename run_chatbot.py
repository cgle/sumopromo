import logging
from chatbot import server

def main():
    logging.basicConfig(level=logging.DEBUG)
    server.start()

if __name__ == '__main__':
    main()
