"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    new_reader = data_reader(fp)

    x = []
    n = 0
    for line in new_reader:
        try:
            (mfg, name, typ) = line
            n += 1
            db.add_bottle_type(mfg, name, typ)
        except ValueError:
            print "New bottle types must have exactly 3 values per line: 'Manufacturer, Name, Type'"

    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    new_reader = data_reader(fp)

    x = []
    n = 0
    for (line) in new_reader:
        try:
            (mfg, name, amount) = line
            n += 1
            db.add_to_inventory(mfg, name, amount)
        except ValueError:
            print "New inventory items must have exactly 3 values per line: 'Manufacturer, Name, Type'"

    return n

def data_reader(fp):
    reader = csv.reader(fp)
    
    for line in reader:
        if not ''.join(line).strip():
            continue
        
        if line[0].startswith('#'):
            continue
        
        yield line

class LineError(Exception):
    pass
