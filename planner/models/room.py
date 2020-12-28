class Room:
    # TODO add exposed variables
    def __init__(self, room_type, min_area, width=None, length=None, adjacent_to=[]):
        """
        Parameters
        ----------

            room_type: RoomType
                type of the room, e.g. RoomType.BEDROOM, RoomType.KITCHEN, etc.

            min_area: int
                Minimum area of the room in square meters

            width: int
                preferred width of the room in meters

            length: int
                Preferred length of the room in meters

            adjacent_to: list
                A list of room indices (in a certain apartment), that this room must be adjacent to one of.
        """
        self.room_type = room_type
        self.min_area = min_area
        self.width = width
        self.length = length
        self.adjacent_to = adjacent_to
        self.variables = None
        self.area_variable = None

    def has_preferred_width(self):
        """ Check if a preferred width was specified """
        return self.width is not None

    def has_preferred_length(self):
        """ Check if a preferred length was specified """
        return self.length is not None

    def has_adjacent_rooms(self):
        """ Check if a adjacent rooms constraint was specified """
        return len(self.adjacent_to) > 0

    def __str__(self):
        return f'Room(room_type={self.room_type}, min_area={self.min_area}, width={self.width}, length={self.length}, adjacent_to={self.adjacent_to}, variables={self.variables})'
