#!/bin/sh
export FLASK_APP=./main.py
pipenv run flask --debug run -h localhost -p 5001