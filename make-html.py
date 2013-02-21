#! /usr/bin/env python

import os
import drinkz.db
import drinkz.recipes

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

drinkz.db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
drinkz.db.add_bottle_type('Evan Williams', 'Cinnamon Reserve', 'kentucky liqueor')

drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
drinkz.db.add_to_inventory('Evan Williams', 'Cinnamon Reserve', '2000 ml')
drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '40oz')

#r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
#drinkz.db.add_recipe(r)

#a = recipes.Recipe('Recipe2', [('blended scotch','6 oz')])
#drinkz.db.add_recipe(r)

bottles = []

for i in drinkz.db._bottle_types_db:
    bottles.append(i)

###

fp = open('html/index.html', 'w')

print >>fp, """
<p>
<a href="recipes.html">Recipes</a>
<br />
<a href="inventory.html">Inventory</a>
<br />
<a href="liquor_types.html">Liquor Types</a>
</p>
"""

fp.close()

###

fp = open('html/liquor_types.html', 'w')

s = ""

for i in bottles:
    s + "<li>" + str(i) + "<li>"

print >>fp, """
<p>
<ul>""" + s
"""</ul>
</p>
"""

fp.close()

###

fp = open('html/inventory.html', 'w')
fp.close()

###

fp = open('html/recipes.html', 'w')
fp.close()