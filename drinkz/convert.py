# Unit conversion to milliliters

# invalid characters to be stripped from amount conversions
_invalid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&\'()*+,-./:;?@[\\]^_`{|}~ "

def to_ml(amt):
    if "ml" in amt or "mL" in amt or "milliliter" in amt or "milliliters" in amt:
        #amt = amt.strip('ml. ')
        amt = amt.strip(_invalid_characters)
        amt = float(amt)
    elif "oz" in amt or "ounce" in amt or "ounces" in amt:
        #amt = amt.strip('oz. ')
        amt = amt.strip(_invalid_characters)
        amt = float(amt)
        amt *= 29.5735
    elif "gal" in amt or "gals" in amt or "gallon" in amt or "gallons" in amt:
        #amt = amt.strip('gallons. ')
        amt = amt.strip(_invalid_characters)
        amt = float(amt)
        amt *= 3785.41
    elif "liter" in amt or "liters" in amt or "L" in amt or "l" in amt:
        amt = amt.strip(_invalid_characters)
        amt = float(amt)
        amt *= 1000
    else:
        amt = float(amt)
    
    return amt