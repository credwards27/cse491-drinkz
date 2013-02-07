import drinkz.db

drinkz.db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
drinkz.db.add_bottle_type('Evan Williams', 'Cinnamon Reserve', 'kentucky liqueor')
drinkz.db.add_bottle_type('Baileys', 'Original', 'irish cream')

drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '40oz')
drinkz.db.add_to_inventory('Evan Williams', 'Cinnamon Reserve', '2000 ml')
drinkz.db.add_to_inventory('Evan Williams', 'Cinnamon Reserve', '500 ml')
drinkz.db.add_to_inventory('Baileys', 'Original', '700 ml')
drinkz.db.add_to_inventory('Baileys', 'Original', '600ml')

print 'Manufacturer\t\tLiquor\t\tAmount'
print '------------\t\t------\t\t------'
for mfg, liquor in drinkz.db.get_liquor_inventory():
    amount = drinkz.db.get_liquor_amount(mfg, liquor)
    print '%s\t\t%s\t\t%s' % (mfg, liquor, amount)