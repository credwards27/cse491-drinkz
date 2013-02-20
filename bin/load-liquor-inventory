#! /usr/bin/env python
import sys
import _mypath
#import drinkz.load_bulk_data

from drinkz.load_bulk_data import load_bottle_types
from drinkz.load_bulk_data import load_inventory

def main(args):
   "Load bottle types and inventory data from files."
   "This script requires 2 arguments: bottle_types_data, inventory_data"
   if len(args) != 3:
      print >>sys.stderr, 'Usage: %s file_to_load.csv'
      return -1

   types_file = args[1]
   inventory_file = args[2]
   
   typ = open(types_file)
   try:
      n = load_bottle_types(typ)
   finally:
      typ.close()
   
   inv = open(inventory_file)
   try:
      m = load_inventory(inv)
   finally:
      inv.close()
   
   print 'Loaded %d bottles types' % n
   print 'Loaded %d bottles to inventory' % m
   return 0
    
# run the 'main()' function if this script is run from the command line;
# this will not execute if the file is imported.
#
# pass in command line arguments verbatim, as a list.

if __name__ == '__main__':
   exit_code = main(sys.argv)
   sys.exit(exit_code)