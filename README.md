[![Build Status](https://secure.travis-ci.org/Moco/django-minidetector.png?branch=master)](http://travis-ci.org/Moco/django-minidetector)

This application is a simple middleware and associated decorator that will add 
a ".mobile" attribute to your request objects, which, if True, means the requester
is coming to you from a mobile phone (cellphone), PDA, or other device that
should be considered small screened, or have an underpowered browser, 
such as games consoles.

This mostly works using a list of search strings, though there are a couple 
of other tricks, like detecting the presence of Opera Mini. The strings are in
an easily-parseable text file, and thus can be used for other similar projects.

It also includes a pretty extensive list of user agents to test against.

It also adds a dictionary to the request object, to figure out which device as 
well as if it's a Facebook app.

To run the tests
================

``` $ python -m unittest minidetector.tests ```
