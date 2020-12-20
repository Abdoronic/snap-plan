class Apartment:
    def __init__(self, rooms):
        """
        Parameters
        ----------
            rooms : list
                list of rooms
        """

        self.rooms = rooms

    def __str__(self):
        return '\t' + '\n\t'.join([str(room) for room in self.rooms])