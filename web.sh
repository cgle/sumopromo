#!/bin/bash

source sumo_env.sh
gunicorn -w 4 -b 127.0.0.1:8000 web:app
