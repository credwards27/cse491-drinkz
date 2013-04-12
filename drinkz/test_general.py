#! /usr/bin/env python
import sys
import simplejson
import urllib2
import StringIO

import drinkz.db
import drinkz.recipes
from drinkz.convert import to_ml
from drinkz.app import SimpleApp

# initialize database
def test_init():
    app = SimpleApp()
    app.load_database('bin/database_file')

# test makeable recipes
def test_get_possible_recipes():
    # this test assumes make-test-database and bulk-load-recipes have been run with the stock files
    # (database_file and bulk_recipes.xml)
    
    recipes = drinkz.db.get_possible_recipes()
    possible = []
    
    for r in recipes:
        possible.append(r)
    
    print possible
    assert possible == ['scotch on the rocks', 'scotch on the rocks 2']
