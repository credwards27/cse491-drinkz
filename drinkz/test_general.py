#! /usr/bin/env python

# this test assumes make-test-database and bulk-load-recipes have been run with the stock files
# (database_file and bulk_recipes.xml)

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
    recipes = drinkz.db.get_possible_recipes()
    possible = []
    
    for r in recipes:
        possible.append(r)
    
    print possible
    assert possible == ['scotch on the rocks']

# test events and venues
def test_events_and_venues():
    events = drinkz.db.get_all_events()
    venues = drinkz.db.get_all_venues()
    
    # add an item to the request list for the event
    events[0].add_to_event('req', 'Johnnie Walker', 'Black Label', '1000 ml')
    
    # get the request list and inventory for the event
    req = events[0].get_all("req")
    inv = events[0].get_all("inv")
    
    # modify the venue's score
    venues[0].add_point()
    venues[0].add_point()
    venues[0].remove_point()
    venues[0].add_point()
    
    assert len(events) == 1, len(venues) == 1
    assert len(events[0].requested_items) == 1, len(events[0].inventory) == 0
    assert req == [('Johnnie Walker', 'Black Label', 1000.0)], inv == []
    assert venues[0].points == 2
