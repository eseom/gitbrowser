#!/usr/bin/env python

from distutils.core import setup

setup(name='flamengo',
      packages=['flamengo', 'flamengo/main', 'flamengo/models', 'flamengo/tasks', 'flamengo/auth', 'flamengo/build'],
      # scripts=['scripts/somescripts.sh'],
      entry_points={
        'console_scripts': [
            'flamengo_celery_runner = flamengo.tasks.runner:run',
        ],
      },
      version='1.0',
      description='source code management server',
      author='eseom <me@eseom.org>',
      include_package_data=True,
      author_email='me@eseom.org',
      url='http://flamengo.io',
      )
