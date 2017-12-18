[![Waffle.io - Columns and their card count](https://badge.waffle.io/peterxie/Crank.png?columns=all)](https://waffle.io/peterxie/Crank?utm_source=badge)
# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  

$ git clone https://github.com/peterxie/Crank.git

$ pipenv install

$ pipenv shell

$ pip install -r requirements.txt

$ python manage.py migrate

$ python crank/fixtures/pop.py    #use this to populate database tables for the first time

$ python manage.py collectstatic

$ python manage.py runserver

## Running on Google Cloud

Log onto Google Cloud using UNI@columbia.edu

Open Console and go to Compute Engine for Project Crank

Under "Remote Access" click on SSH. This opens up shell to the VM instance.

Clone github. The rest of the steps are the same as running locally except one.

To run on google cloud for public access

$ python manage.py runserver 0:8000
