# implementation of events

from datetime import date
from datetime import time

import db

# event class object
class Event(object):
    def __init__(self):
        self.name = ""
        self.host = ""
        self.venue = None
        self.date = date.today()
        self.time = time(19,0)
        
        self.requested_items = {}
        self.inventory = {}
    
    # add a liquor type and amount to requested items or event inventory
    # dest indicates if liquor is being requested or added to inventory ("req" or "inv")
    def add_to_event(self, dest, mfg, liq, amt):
        if not dest == "req" and not dest == "inv":
            print "The 'dest' parameter must be 'req' or 'inv'"
            return
        
        if not db._check_bottle_type_exists(mfg, liq):
            err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liq)
            raise db.LiquorMissing(err)
        
        if dest == "req":
            if not self.check_requests(mfg, liq):
                self.requested_items[(mfg, liq)] = db.to_ml(amt)
            else:
                self.requested_items[(mfg, liq)] += db.to_ml(amt)
        elif dest == "inv":
            if not self.check_inventory(mfg, liq):
                self.inventory[(mfg, liq)] = db.to_ml(amt)
            else:
                self.inventory[(mfg, liq)] += db.to_ml(amt)
    
    # get a list of all requested liquor types
    # list indicates if retrieving the request list or inventory ("req" or "inv")
    def get_all(self, list):
        if not list == "req" and not list == "inv":
            print "The 'list' parameter must be 'req' or 'inv'"
            return
        
        returnList = []
        if list == "req":
            for (m,l) in self.requested_items.keys():
                returnList.append((m,l,self.requested_items[(m,l)]))
        elif list == "inv":
            for (m,l) in self.inventory.keys():
                returnList.append((m,l,self.inventory[(m,l)]))
        return returnList
    
    # check if the liquor type has already been requested
    def check_requests(self, mfg, liq):
        for (m,l) in self.requested_items.keys():
            if mfg == m and liq == l:
                return True
        return False
    
    # check if the liquor type has already been added to the event inventory
    def check_inventory(self, mfg, liq):
        for (m,l) in self.inventory.keys():
            if mfg == m and liq == l:
                return True
        return False
