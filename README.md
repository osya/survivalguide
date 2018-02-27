# README

## Introduction

[![Build Status](https://travis-ci.org/osya/survivalguide.svg)](https://travis-ci.org/osya/survivalguide) [![Coverage Status](https://coveralls.io/repos/github/osya/survivalguide/badge.svg?branch=master)](https://coveralls.io/github/osya/survivalguide?branch=master)

Django-based app created during the video [Kenneth Love: Getting Started with Django, a crash course - PyCon 2014](https://www.youtube.com/watch?v=KZHXjGP71kQ)

Used technologies:

- Python & Django
- Testing: Selenium & Headless Chrome & Factory Boy
- Assets management: NPM & Webpack
- Travis CI
- Deployed at [Heroku](https://django-survival-guide.herokuapp.com/talks/lists/)

## Installation

```shell
    git clone https://github.com/osya/survivalguide
    cd survivalguide
    pip install -r requirements.txt
    npm install
    node node_modules/webpack/bin/webpack.js
    python manage.py collectstatic
    python manage.py runserver
```

## Usage

## Tests

To run all tests, run

```shell
    python manage.py test
```
