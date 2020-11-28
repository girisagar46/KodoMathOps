# KodoMathOps

[![Build Status](https://travis-ci.org/girisagar46/KodoMathOps.svg?branch=master)](https://travis-ci.org/girisagar46/KodoMathOps)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

A Backend API for a MVP of an application to learn the basic mathematical operations. Developed for the company KodoMath.. Check out the project's [documentation](http://girisagar46.github.io/KodoMathOps/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

# Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```
