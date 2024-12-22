#!/bin/sh
export FLASK_APP=./api.py
pipenv run flask --debug run -h localhost -p 5001