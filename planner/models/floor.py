from planner.models.apartment import Apartment


class Floor:
    def __init__(self, width, length, sides_views, apartments):
        """
        Parameters
        ----------

            width : int
                width of the floor
            
            length : int
                length of the floor
            
            sides_views : 4-tuple
                floor Views at its 4 sides (N,S,E,W)
            
            apartments : list
                list of apartments
        """

        self.width = width
        self.length = length
        self.sides_views = sides_views
        self.apartments = apartments


    @property
    def rooms(self):
        rooms = []
        for apartment in self.apartments:
            rooms.append(apartment.rooms)
        return rooms

    def __str__(self):
        floor_repr = f'Floor(width={self.width}, length={self.length}, sides_views={self.sides_views},\n'
        floor_repr += 'apartments=[\n' + '\n\n'.join([str(apartment) for apartment in self.apartments]) + '\n])'
        return floor_repr
    
