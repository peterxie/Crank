# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  

$ git clone https://github.com/peterxie/Crank.git
$ pipenv install
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py runserver
