#!/bin/sh
python3virtualenv=`which pyvenv`
test "$python3virtualenv" = "" && { echo ensure the python3 path; exit 1; }
test ! -d ve && $python3virtualenv ve
ve/bin/pip install --upgrade pip
ve/bin/pip install -r requirements.txt

bower install
cd flamengo/static/web
bower install
