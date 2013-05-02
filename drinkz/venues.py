# implementation of venues

# venue class object
class Venue(object):
    def __init__(self):
        self.name = ""
        self.address = ""
        self.city = ""
        self.state = ""
        self.zipcode = 0
        self.description = ""
        self.points = 0
        
    def add_point(self):
        self.points += 1
        
    def remove_point(self):
        self.points -= 1
