#!/bin/bash

source venv/bin/activate
gunicorn -w 4 -b 127.0.0.1:8080 launching_page:app
