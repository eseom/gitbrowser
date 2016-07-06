# Flamengo

Flamengo is a flask and angular based web project like Github.

[![Build Status](https://travis-ci.org/eseom/flamengo.svg)](https://travis-ci.org/eseom/flamengo)

## requirements

* python>=3.5.1
* git>=2.7.4

## instance test

```
sudo npm install -g bower
sh scripts/setup.sh
ve/bin/python manage.py db upgrade
ve/bin/python manage.py devserver
open http://localhost:5000
```

## development environment
* repo directory: {project_root}/instance/repo
* repo database: /tmp/flamengo.database (sqlite3)

## unittest

```
nosetests
```
